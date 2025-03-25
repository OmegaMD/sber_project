function push_location_info(img_url) {
    const box = document.getElementById('location_info_box');
    box.style.padding = "10px";
    const new_element = document.createElement('div');
    new_element.className = 'block appearing';
    new_element.style.overflow = 'hidden';
    // new_element.innerHTML = '<img class="" style="width: 100%" src="' + img_url + '"></img>';

    const img = document.createElement('img');
    img.src = img_url;
    img.style.width = "100%";
    img.style.maxWidth = "none";
    img.style.maxHeight = "none";
    img.style.borderRadius = "20px";

    new_element.appendChild(img);

    box.appendChild(new_element);

    img.onload = function() {
        new_element.style.height = new_element.scrollHeight * 2 + 'px';

        setTimeout(() => {
            new_element.classList.add('show');
        }, 10);
    };
    /*
    box.style.padding = "10px";
    box.innerHTML = '\
    <div class="block appearing show">\
        <img class="expand-img" src="' + img_url + '"></img>\
    </div>\
    ';
    */
}

function pop_location_info() {
    const box = document.getElementById('location_info_box');
    box.style.padding = "0";
    box.innerHTML = '';
}