//create_time: 2019/7/8 22:13
$(function() {
    $('#save-banner-btn').click(function(event) {
        var self = $(this);
        event.preventDefault();
        var dialog = $('#banner-dialog');
        var name_input = $('input[name="name"]');
        var image_url_input = $('input[name="image_url"]');
        var link_url_input = $('input[name="link_url"]');
        var priority_input = $('input[name="priority"]');

        var name = name_input.val();
        var image_url = image_url_input.val();
        var link_url = link_url_input.val();
        var priority = priority_input.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr('data-id');
        if (!name || !image_url || !link_url || !priority) {
            zlalert.alertInfoToast('请输入完整的轮播图数据！');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/ubanner/';
        } else {
            url = '/cms/abanner/';
        }
        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function(data) {
                dialog.modal('hide');
                if (data['code'] == 200) {
                    //重新加载这个页面
                    window.location.reload();
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function(error) {
                zlalert.alertNetworkError();
            }
        });
    })
});

$(function() {
    $('.edit-banner-btn').click(function(event) {
        var self = $(this);
        event.preventDefault();
        var dialog = $('#banner-dialog');
        dialog.modal('show');
        var tr = self.parent().parent();

        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        var name_input = dialog.find('input[name="name"]');
        var image_url_input = dialog.find('input[name="image_url"]');
        var link_url_input = dialog.find('input[name="link_url"]');
        var priority_input = dialog.find('input[name="priority"]');
        var save_btn = dialog.find('#save-banner-btn');
        name_input.val(name);
        image_url_input.val(image_url);
        link_url_input.val(link_url);
        priority_input.val(priority);
        save_btn.attr('data-type','update');
        save_btn.attr('data-id',tr.attr('data-id'));
    })
});

$(function() {
    var $close_btn = $('.close-btn');
    $close_btn.click(function() {
       $('#save-banner-btn').removeAttr('data-type');
       var name_input = $('input[name="name"]');
       var image_url_input = $('input[name="image_url"]');
       var link_url_input = $('input[name="link_url"]');
       var priority_input = $('input[name="priority"]');
       name_input.val('');
       image_url_input.val('');
       link_url_input.val('');
       priority_input.val('');
   })
});

$(function() {
    $('.delete-banner-btn').click(function(event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr('data-id');
        zlalert.alertConfirm({
            'msg': '您确认要删除这个轮播图吗？',
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dbanner/',
                    'data': {
                        'banner_id': banner_id
                    },
                    'success': function(data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    })
})

$(function() {
    zlqiniu.setUp({
        'domain': 'http://pud1g0cic.bkt.clouddn.com/',
        'browse_btn': 'upload-btn',
        'uptoken_url': '/c/uptoken/',
        'success': function(up,file,info) {
            var imageInput = $('input[name="image_url"]');
            imageInput.val(file.name);
        },
    });
})