function reg_add(){
   				uname = document.add.name.value; //姓名
                umail = document.add.mail.value; //email
                tag = true;
                if(uname == ''){
                     alert('Please input your name. 請輸入姓名');
                     tag = false;
                }
                if(umail == ''){
                     alert('Please input your name. 請輸入E-mail');
                     tag = false;
                }
                if(tag)
                    document.add.submit();
}
