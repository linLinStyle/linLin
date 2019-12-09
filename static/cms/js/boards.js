//create_time: 2019/7/9 21:54
$(function() {
    $('#add-board-btn').click(function() {
        zlalert.alertOneInput({
            'text': '请输入要添加的板块名称',
            'placeholder': '板块名称',
            'confirmCallback': function(inputValue) {
                zlajax.post({
                    'url': '/cms/aborder/',
                    'data': {
                        'name': inputValue
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
    });

    $('.edit-board-btn').click(function(event) {
        var self = $(this);
        event.preventDefault();
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');
        var name = tr.attr('data-name');
        zlalert.alertOneInput({
            'text': '请输入您想要修改成的板块名称',
            'placeholder': name,
            'confirmCallback': function(inputValue) {
                zlajax.post({
                    'url': '/cms/uborder/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
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
    });

    $('.delete-board-btn').click(function(event) {
        var self = $(this);
        event.preventDefault();
        zlalert.alertConfirm({
            'msg': '您确认要删除这个板块吗？',
            'confirmCallback': function() {
                var tr = self.parent().parent();
                var board_id = tr.attr('data-id');
                zlajax.post({
                    'url': '/cms/dborder/',
                    'data': {
                        'board_id': board_id
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
