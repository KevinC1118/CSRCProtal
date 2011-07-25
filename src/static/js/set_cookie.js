	   function saveName(editor)
       {
          now=new Date() ;
　 		  now.setTime(now.getTime() + 1000 * 60 * 60 * 24 * 30) ;

          document.cookie = "User=" + editor + ";expires=" + now.toGMTString() ;
          
       }
       
       function getUserName(editor)
       {
          split_cookie = document.cookie.split("User=");
          dobule_split = split_cookie[1].split("; expire") ;
          document.getElementById(editor).value = dobule_split[0];
          document.getElementById('editor1').value = dobule_split[0];
       }