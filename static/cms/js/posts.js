//create_time: 2019/7/12 12:16
$(function() {
   $('.heightlight-btn').click(function() {
       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('data-id');
       var heightlight = parseInt(tr.attr('data-heightlight'));
       var url = '';
       if (!heightlight) {
           url = '/cms/hpost/'
       } else {
           url = '/cms/uhpost/'
       }
       zlajax.post({
           'url': url,
           'data': {
               'post_id': post_id
           },
           'success': function(data){
               if (data['code'] == 200) {
                   zlalert.alertSuccessToast('操作成功！');
                   setTimeout(function() {
                       window.location.reload();
                   },500)
               } else {
                   zlalert.alertInfo(data['message']);
               }
           }
       });
   })
});