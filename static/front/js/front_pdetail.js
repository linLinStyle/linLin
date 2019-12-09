//create_time: 2019/7/11 16:43
$(function() {
   ue = UE.getEditor('editor',{
       'serverUrl': '/ueditor/upload/',
       'toolbars': [[
           //数组里面的数组，一个代表一行
           'bold', //加粗
           'italic', //斜体
           'blockquote', //引用
           'selectall', //全选
           'cleardoc', //清空文档
           'fontfamily', //字体
           'fontsize', //字号
           'simpleupload', //单图上传
           'emotion', //表情

       ]]
   });
   window.ue = ue;
});

$(function () {
    $('#comment-btn').click(function(event) {
        event.preventDefault();
        var is_login = $('.login-tag').attr('data-login');
        if (is_login) {
            var content = window.ue.getContent();
            var post_id = $('#post-id-tag').attr('data-id');
            zlajax.post({
                'url': '/acomment/',
                'data': {
                    'content': content,
                    'post_id': post_id
                },
                'success': function(data) {
                    if (data['code'] == 200) {
                        window.location.reload();
                    } else{
                        zlalert.alertInfo(data['message']);
                    }
                },
            });
        } else {
            window.location = '/signin/';
        }
    })
})