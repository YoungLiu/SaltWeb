function createXmlHttp() {
    var xmlHttp = null;
    try {
        //Firefox, Opera 8.0+, Safari
        xmlHttp = new XMLHttpRequest();
    } catch (e) {
        //IE
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    return xmlHttp;
}

function editTemplate(filename, filecontent) {
    document.getElementById('editModalLabel').value = filename;
    filecontent = filecontent.replace(/ /g, "\r\n")
    document.getElementById('editModalContent').value = filecontent;
}

function addTemplate(){
    filename = document.getElementById('editModalLabel').value
    filecontent = document.getElementById('editModalContent').value
    var xmlHttp = createXmlHttp();
    if (!xmlHttp) {
        alert("您的浏览器不支持AJAX！");
        return 0;
    }
    var url = "/hosts/template/edit";
    var postdata = "templatename=" + filename + "&templatecontent=" + filecontent;
    xmlHttp.open("POST", url, true);
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xmlHttp.send(postdata);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            //tip.innerHTML = xmlHttp.responseText;
            var PostAnswer = xmlHttp.responseText;
            if (PostAnswer == "Edit.True")
            {
                alert("添加成功！");
                window.location.href = "/hosts/template";
            }
            else if (PostAnswer == "Error") {
                alert("貌似服务器出错了噢(┬＿┬)！");
                //document.userForm.reset();
                //username.focus();;
                return false;
            }
            else {
                alert("服务器也木有知道哪儿出错了(┬＿┬)");
                //document.userForm.reset();
                //username.focus();
                return false;
            }
        }
    }
}


// hosts页面按照条件刷选显示
function onSearch(selectID, row) {//js函数开始
    setTimeout(function () {//因为是即时查询，需要用setTimeout进行延迟，让select选定时，再读取
        var storeId = document.getElementById('datalist');//获取table的id标识
        var rowsLength = storeId.rows.length - 1;//表格总共有多少行，这里减1表示去除最后一行footer标题
        //var key = obj.value;//获取输入框的值
        var select = document.getElementById(selectID)
        var key = select.options[select.selectedIndex].value;     //获取select的值
        var searchCol = row;//要搜索的哪一列，这里用变量row

        for (var i = 1; i < rowsLength; i++) {//按表的行数进行循环，第一行是标题不计算在内，所以i=1，从第二行开始筛选（从0数起）
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;//取得table行，列的值

            if (searchText.match(key)) {//用match函数进行筛选，如果input的值，即变量 key的值为空，返回的是true，
                storeId.rows[i].style.display = '';//显示行操作，
            } else {
                storeId.rows[i].style.display = 'none';//隐藏行操作
            }
        }
    }, 100);//100为延时时间，这里是100毫秒
}