from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from file.youtube import clientLogin, YOUTUBE_DEFAULT_USER_FEED_URI
import cgi
import gdata.media
import gdata.youtube


def upload(request):
    client = clientLogin()
     
    if request.method == 'POST':
        video_title = cgi.escape(request.POST['video_title'])
        video_description = cgi.escape(request.POST['video_description'])
        video_category = cgi.escape(request.POST['video_category'])
        video_tags = cgi.escape(request.POST['video_tags'])
            
        my_media_group = gdata.media.Group(
           title = gdata.media.Title(text=video_title),
            description = gdata.media.Description(description_type='plain',
                                                  text=video_description),
            keywords = gdata.media.Keywords(text=video_tags),
            category = gdata.media.Category(
                            text=video_category,
                            scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
                            label=video_category)
        )
            
        video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
            
        server_response = client.GetFormUploadToken(video_entry)
            
        return render_to_response('file/youtube/upload_file_form.html', 
                                  {'post_url' : server_response[0], 
                                   'next_url' : 'http://' + request.get_host() + '/file/youtube/upload/result', 
                                   'youtube_token' : server_response[1]})
        
    else:
        return render_to_response('file/youtube/upload_form.html')   
        
        
def uploadResult(request):
    upload_status = request.GET.get('status', None)
    new_video_id = request.GET.get('id', None)
    
    if upload_status:
        if upload_status == '200':
            client = clientLogin()
            
            message = 'Upload successful.<br />'
                
            player_url = 'http://www.youtube.com/watch?v=' + new_video_id
            link_code = '<a href="%s">%s</a>' % (player_url, player_url)
                
            entry = client.GetYouTubeVideoEntry(video_id=new_video_id)
            if entry.GetSwfUrl():
                swf_url = entry.GetSwfUrl()
                embed_code = (
                    '<object width="425" height="350">'
                        '<param name="movie" value="%s"></param>'
                        '<embed src="%s" '
                            'type="application/x-shockwave-flash" width="425" height="350"></embed>'
                    '</object>' % (swf_url, swf_url)
                    )
        else:
            message = 'Upload failed.<br />' + \
                      'Video upload status: ' + upload_status
                      
        return render_to_response('file/youtube/upload_result.html', 
                                  {'message' : message, 
                                   'link_code' : link_code, 
                                   'embed_code' : embed_code})
    else:
        return HttpResponseRedirect('/file/youtube/upload')
    
    
def delete(request):
    
    video_id = request.POST.get('video_id', None)
    next_url = request.POST.get('next_url', None)
    
    if video_id and next_url:
        client = clientLogin()
        
        client.Delete(uri=YOUTUBE_DEFAULT_USER_FEED_URI+'/'+video_id)
        
        return HttpResponseRedirect(next_url)
    
    else:
        return HttpResponse('Error!')
