function gamesDiv(games) {
    let gamesHTML = "<div class='row center'>";

    games.forEach(function(game) {
        gamesHTML += `
            <div class='column-bottom'>
                <img src='${game.image}' alt='Cover for: ${game.title}' height='150' />
                <h3>${game.title}</h3>
            </div>
        `;
    });

    return gamesHTML + "</div>";
}

function filtersTable(genres, tags, platforms) {
    return `
        <table>
            <tr> <th> Genre(s) </th> <td> ${genres} </td> </tr>
            <tr> <th> Tag(s) </th> <td> ${tags} </td> </tr>
            <tr> <th> Platform(s) </th> <td> ${platforms} </td> </tr>
        </table>
    `;
}

$(function() {
    $("#confirm").on("click", function() {
        $("#filters").hide();
        $("#confirm_form").hide();
        $("#similar_games").hide();

        let genre = $("#genre").val(), tag = $("#tag").val(), platform = $("#platform").val()
        let gameIds = ['id_1', 'id_2', 'id_3'].map(id => $('#' + id).val()).filter(id => id);

        if (gameIds.length > 0) {
            $.ajax({
                url: '/fetch_game_details',
                type: 'GET',
                traditional: true, 
                data: {ids: gameIds, genre: genre, tag: tag, platform: platform},
                success: function(returned_data) {
                    if (returned_data.error) { alert(returned_data.error); }
                    else {
                        $("#similar_games").html(gamesDiv(returned_data.games));
                        $("#similar_games").show();

                        $("#filters").html(
                            filtersTable(returned_data.genres_names, returned_data.tags_names, returned_data.platforms_names)
                        );
                        $("#filters").show();

                        $('#similar_genres').val(returned_data.genres_ids);
                        $('#similar_tags').val(returned_data.tags_ids);
                        $('#similar_platforms').val(returned_data.platforms_ids);

                        $("#confirm_form").show();
                    }
                },
                error: function() { alert('An Error Occured While Fetching Game Details'); }
            });
        }
        else {
            let userGenre = genre.split("|"), userTag = tag.split("|"), userPlatform = platform.split("|");

            $('#similar_genres').val(userGenre[1]);
            $('#similar_tags').val(userTag[1]);
            $('#similar_platforms').val(userPlatform[1]);

            $("#filters").html(filtersTable(userGenre[0], userTag[0], userPlatform[0]));
            $("#filters").show();

            $("#confirm_form").show();
        }
    });

    $("[id*='limit_']").on("click", function() {
        $("[id*='limit_']").removeClass("active");
        $(this).addClass("active");

        let limit = $(this).attr("id").split("_")[1]
        $("#search_limit").val(limit);
    });
});