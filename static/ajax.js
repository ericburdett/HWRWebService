function get_journal_entries() {
    var xmlhttp = new XMLHttpRequest();

    var url = '/inferences'

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === XMLHttpRequest.DONE) {
            if (xmlhttp.status === 200) {
                var result = JSON.parse(xmlhttp.responseText);

                console.log(result)

                html = '<div class="card-columns">'

                for (var i = 0; i < result.length; ++i) {
                    var img = result[i].img
                    img = img.replaceAll('-', '+')
                    img = img.replaceAll('_', '/')

                    var transcription = result[i].transcription

                    html += '<div class="card">'
                        + '<img class="card-img-top" src="' + img + '" alt="' + transcription + '">'
                        + '<div class="card-body"><h6 class="card-text">' + transcription + '</h6></div>'
                        + '</div>'
                }

                html += '</div>'

                document.getElementById('inferences').innerHTML = html;
            }
        }
    };
    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function predict() {
    document.getElementById('upload-button').innerHTML = "<span class=\"spinner-border spinner-border-sm\"></span> Upload"

    var img_data = document.getElementById('img-upload').src

    img_data = img_data.replaceAll('+', '-')
    img_data = img_data.replaceAll('/', '_')

    var xmlhttp = new XMLHttpRequest();
    var url = '/predict'

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === XMLHttpRequest.DONE) {
            if (xmlhttp.status === 200) {
                alert('Image has been uploaded successfully.')
            }
            else {
                alert('There was an error uploading the image.')
            }
            document.getElementById('upload-button').innerHTML = "Upload"
        }
    };
    xmlhttp.open('POST', url, true);
    xmlhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xmlhttp.send("img=" + img_data);
}