function doUpload() {
    var formData = new FormData($("#ajaxfm")[0]);
    $.ajax({
        url: "/api/v1/goods/",
        type: "POST",
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            $.messager.alert("提示", "增加成功！");
            $("#dd").dialog('destroy');
            location.reload();
        },
        error: function (data) {
            console.log(data);
        },
    });
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}


$(function () {

    $.ajaxSetup({
        headers: {"X-CSRFToken": getCookie("csrftoken"), "csrftoken": getCookie("csrftoken")},
    });

    $('#dg').datagrid({
        url: '/api/v1/goods/',
        method: 'get',
        pagination: true,
        fitColumns: true,
        scrollbarSize: 4,
        toolbar: "#tool",
        columns: [[
            {field: 'check', title: '复选框', checkbox: true, width: 100, align: 'center'},
            {field: 'goods_sn', title: '商品唯一序列号', width: 100, align: 'center'},
            {field: 'name', title: '商品名', width: 100, align: 'center'},
            {field: 'key', title: '商品关键字', width: 100, align: 'center'},
            {
                field: 'image', title: '图片', width: 100, align: 'center', height: 100,
                formatter: function (value, row, index) {
                    if (value) {
                        return "<a href=" + value + " " + "download " + "=download" + ">" + "下载" + "</a>";
                    }
                }
            },
            {field: 'priority', title: '优先级', width: 100, align: 'center'},
            {field: 'file_address', title: '本地文件地址', width: 100, align: 'center'},
        ]]
    });
    $('#tb').textbox({
        buttonText: '搜索',
        iconCls: 'icon-search',
        iconAlign: 'left',
        onClickButton: function () {
            $('#dg').datagrid({
                queryParams: {
                    search: $("#tb").val(),
                }
            });
        }
    });
    //删除
    $("#btnDelete").linkbutton({
        onClick: function () {
            var rows = $("#dg").datagrid("getChecked");  // 多个
                if (rows.length == 0) {
                    $.messager.alert('警告', '请选择删除的数据！');
                } else {

                    var goods_sn = "";
                    var data = "";
                    for (var i = 0; i < rows.length; i++) {
                        if (i < rows.length - 1) {
                            data += rows[i + 1].goods_sn + ",";
                            goods_sn = rows[0].goods_sn;
                        } else {
                            goods_sn = rows[0].goods_sn;
                        }

                    }

                    console.info(goods_sn);
                    var data = data.substring(0, data.length - 1);
                    console.info(data);
                    $.messager.confirm('确认', '您确认想要删除记录吗？', function (r) {
                        if (r) {
                            $.ajax({
                                url: '/api/v1/goods/' + goods_sn + '/',
                                type: 'delete',
                                data: {
                                    goods_sns: data,
                                },
                                success: function (data, textStatus, jqXHR) {
                                    console.info(jqXHR); // 其余两个值都是为undefined
                                    if (jqXHR.status == 204) {
                                        $.messager.alert('提示', '删除成功！');
                                        $("#dg").datagrid("reload");
                                    } else {
                                        $.messager.alert('提示', '删除失败！');
                                    }
                                }

                            });
                        }
                    });


                }
            }
        });
    //编辑
    $("#btnEdit").linkbutton({
        onClick: function () {

            var rows = $("#dg").datagrid("getSelections");
            if (rows.length == 0 || rows.length > 1) {
                $.messager.alert("提示", "请选择一行数据");
            } else {
                $('#dd').dialog({
                    title: '修改信息',
                    width: 400,
                    height: 400,
                    closed: false,
                    cache: false,
                    modal: true,
                });
                $("#btn-add").hide();
                $("#btn").show();
                var goods_sn = rows[0].goods_sn
                var name = rows[0].name
                var key = rows[0].key
                var priority = rows[0].priority
                var file_address = rows[0].file_address
                $("#goods_sn").textbox({
                    value: goods_sn
                });
                $("#name").textbox({
                    value: name
                });
                $("#key").textbox({
                    value: key
                });
                $("#priority").textbox({
                    value: priority
                });
                $("#file_address").textbox({
                    value: file_address
                });

                $("#btn").linkbutton({
                    onClick: function () {

                        var form = new FormData($("#ajaxfm")[0]);
                        $.ajax({
                            headers: {
                                'X-HTTP-Method-Override': 'PATCH'
                            },
                            url: '/api/v1/goods/' + goods_sn + '/',
                            type: 'PATCH',
                            contentType: false, // 告诉jQuery不要去设置Content-Type请求头
                            processData: false, // 告诉jQuery不要去处理发送的数据
                            data: form,
                            success: function (data, textStatus, jqXHR) {
                                console.log('edit success');
                                console.log(data);  // 有数据了
                                console.log(jqXHR.status)
                                if (jqXHR.status == 200) {
                                    $.messager.alert("提示", "修改成功！");
                                    $("#dd").dialog('destroy');
                                    location.reload();
                                } else {
                                    console.log(data);
                                    $.messager.alert("提示", "修改失败！");
                                }
                            }
                        ,
                            error: function (data) {
                                console.log('edit error');
                                console.log(data);
                            }
                        ,
                        }
                    )
                        ;
                    }
                })
            }
        }
    });

    // 添加
    $("#btnAdd").linkbutton({
        onClick: function () {
            $("#dd").dialog({
                width: 500,
                height: 400,
                title: "添加商品",
            });
            $("#btn").hide();
            $("#btn-add").show();
            $("#btn").linkbutton({
                onClick:
                    function () {
                        $.ajax({
                            url: '/api/v1/goods/',
                            type: 'post',
                            data: {
                                goods_sn: $("#goods_sn").val(),
                                name: $("#name").val(),
                                key: $("#key").val(),
                                priority: $("#priority").val(),
                                image: $("#image").prop("files")[0],
                                file_address: $("#file_address").val(),
                            },
                            success: function (res) {
                                if (res == 1) {
                                    $.messager.alert("提示", "添加成功！");
                                } else {
                                    $.messager.alert("提示", "添加失败！");
                                }
                            }
                        })
                    }
            });
        }
    })

})

