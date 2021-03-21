$("button[name='btn_delete_function']").click(function() {

    var data = { function_name : $(this).data('function_name')}

    $.ajax({
      type: 'POST',
      url: "/delete_function",
      data: data,
      dataType: "text",
      success: function(resultData) {
          location.reload();
      }
});
});


$("button[name='btn_edit_function']").click(function() {

    window.location = "edit_function?function_name="+$(this).data('function_name');

});


$("button[name='btn_new_testcase']").click(function() {

    window.location = "new_testcase/"+$(this).data('function_name');

});


$("button[name='btn_new_correlation']").click(function() {

    window.location = "correlation/"+$(this).data('function_name');

});


$("button[name='btn_new_clustering']").click(function() {

    window.location = "clustering/"+$(this).data('function_name');

});


$("button[name='btn_new_tests']").click(function() {

    window.location = "testing/"+$(this).data('function_name');

});

$("button[name='btn_function_details']").click(function() {

    window.location = "testcase/"+$(this).data('function_name');

});



