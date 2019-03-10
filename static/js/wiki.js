/**
 * Created by IntelliJ IDEA.
 * Project: Jaram-Professor-Crawler
 * ===========================================
 * User: ByeongGil Jung
 * Date: 2019-01-19
 * Time: 오전 3:27
 */

$(document).ready(function() {
    // Params
    let context = null;

    // When init rendering page (at first)
    $.ajax({
        type: "POST",
        url: "/wiki/get",
        data: {prof_name: $("#prof_name").text()},
        datatype: "JSON",
        success: function(data) {
            context = data["context"];
            $("#context").text(context);
        },
        error: function(xhr, status, error) {
            console.log("Occurring error when init rendering page");
            console.log(error);
        }
    });

    // When writing wiki
    $("#wiki_write_btn").click(function() {
        if ($("#switch").val() === "False") {
            $("#switch").val("True");
            $("#wiki_write_btn").text("수정 완료");
            $("#context").replaceWith("<textarea id='context' rows='15' cols='80'>" + context + "</textarea>");
        } else {
            $.ajax({
                type: "POST",
                url: "/wiki/write",
                data: {
                    prof_name: $("#prof_name").text(),
                    context: $("#context").val()
                },
                datatype: "JSON",
                success: function (data) {
                    context = data["context"];

                    $("#context").replaceWith("<textarea id='context' readonly='readonly' rows='15' cols='80' style='border: 0; resize: none;'>" + context + "</textarea>");
                    $("#wiki_write_btn").text("위키 작성");
                    $("#switch").val("False");
                },
                error: function (xhr, status, error) {
                    console.log("Occurring error when input wiki text");
                    console.log(error);
                }
            });
        }
    });
});