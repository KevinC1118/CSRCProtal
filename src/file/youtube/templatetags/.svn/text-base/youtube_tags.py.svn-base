from django import template
import datetime


register = template.Library()


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.tag(name="format_local_time")
def do_format_local_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, date_to_be_formatted, old_format_string, time_difference, new_format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly four arguments" % token.contents.split()[0])
    if not (old_format_string[0] == old_format_string[-1] and old_format_string[0] in ('"', "'") and 
            new_format_string[0] == new_format_string[-1] and new_format_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    return FormatLocalTimeNode(date_to_be_formatted, old_format_string[1:-1], time_difference, new_format_string[1:-1])


class FormatLocalTimeNode(template.Node):
    def __init__(self, date_to_be_formatted, old_format_string, time_difference, new_format_string):
        self.date_to_be_formatted = template.Variable(date_to_be_formatted)
        self.old_format_string = str(old_format_string)
        self.time_difference = int(time_difference)
        self.new_format_string = str(new_format_string)

    def render(self, context):
        try:
            actual_date = self.date_to_be_formatted.resolve(context)
            standard_date = datetime.datetime.strptime(actual_date, 
                                                       self.old_format_string)
            local_date = standard_date + datetime.timedelta(hours=self.time_difference)
            return local_date.strftime(self.new_format_string)
        except template.VariableDoesNotExist:
            return ''
