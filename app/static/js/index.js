$(function() {
    // Confirmation function
    $("#confirm").on("click", function() {
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
                        alert("Genres: " + returned_data.genres);
                        alert("Tags: " + returned_data.tags);
                        alert("Platforms: " + returned_data.platforms);

                        $('#similar_genres').val(returned_data.genres);
                        $('#similar_tags').val(returned_data.tags);
                        $('#similar_platforms').val(returned_data.platforms);
                    }
                },
                error: function() { alert('An Error Occured While Fetching Game Details'); }
            });
        }
        else {
            alert(`Selected Filters: [Genre: ${genre} | Tag: ${tag} | Platform: ${platform}]`)
            $('#similar_genres').val(genre);
            $('#similar_tags').val(tag);
            $('#similar_platforms').val(platform);
        }
    });
});