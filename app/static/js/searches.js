$(function() {
    $("[id*='btn_']").on("click", function() {
        $("#searchForm").hide();

        num = $(this).attr("id").split("_")[1];
        ids = $("#game_" + num).text();

        $("#game_ids").val(ids);
        $("#searchForm").show();
    });
});