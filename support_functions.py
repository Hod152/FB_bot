
def parse_date_str_to_num(date_as_str):
    """
    date_as_str format : "July 6, 2020 at 4:14 AM"
    output format : YYYYMMDDHHSS
    """
    date_parser = date_as_str.split(' at ')
    # parse year
    date_num = str(date_parser[0][-4:])
    month_dict = {'January' : '01' ,
                        'February' : '02' , 
                        'March' : '03' ,
                        'April' : '04' , 
                        'May' : '05' ,
                        'June' : '06' ,
                        'July' : '07' ,
                        'August' : '08' ,
                        'September' : '09' ,
                        'October' : '10' ,
                        'November' : '11' , 
                        'December' : '12' }
    # parse month
    for key, val in month_dict.items():
        if key in date_as_str:
            date_num = date_num + str(val)
            break
    # parse day
    day = date_parser[0].split(',')[0].split(' ')[1]
    if len(day) < 2:
        date_num = date_num + '0' + day
    else:
        date_num += day
    # parse hour
    hour = int(date_parser[1].split(':')[0])
    if 'PM' in date_parser[1]:
        hour = hour + 12
        if hour == 24:
            hour = 0
    elif hour < 10 :
        hour = "0" + str(hour)
    hour = str(hour)
    date_num += hour
    #parse seconds
    sec = date_parser[1].split(':')[1]
    sec = sec.split(' ')[0]
    if int(sec) < 10 :
        sec = "0" + sec
    date_num += sec
    
    return str(date_num)

def currentFrame(self):
        return str(self.execute_script("""
            var frame = window.frameElement;
            if (!frame) {
                return 'root of window named ' + document.title;
            }
            var ret   = '<' + frame.tagName;
            if (frame.name) {
                ret += ' name=' + frame.name;
            }
            if (frame.id) {
                ret += ' id=' + frame.id;
            }
            return ret + '>';
            """))