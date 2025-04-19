function show_filters() {
    const box = document.getElementById('location_info_box');

    if (!box.hasChildNodes()) {
        // box.style.padding = "10px";
        const new_element = document.createElement('div');
        new_element.className = 'column appearing';
        new_element.style.overflow = 'hidden';
        // new_element.innerHTML = '<img class="" style="width: 100%" src="' + img_url + '"></img>';

        // const img = document.createElement('img');
        // img.src = 'https://wallpapers.com/images/featured/cool-skull-pictures-oi8h4846tbciuosj.webp';
        // img.style.width = "100%";
        // img.style.maxWidth = "none";
        // img.style.maxHeight = "none";
        // img.style.borderRadius = "20px";
        // new_element.appendChild(img);

        const symbols = ['restaurant', 'pill', 'local_gas_station', 'shopping_bag'];
        const types = ['кафе', 'аптека', 'заправка', 'магазин'];

        const rows = [];

        i = 0;
        types.forEach(type => {
            if (i % 4 == 0) {
                rows.push(document.createElement('form'));
                rows.at(-1).className = 'row';
                rows.at(-1).style.height = 'auto';
                rows.at(-1).style.aspectRatio = '5';

                rows.at(-1).method = 'post';
                rows.at(-1).action = 'map';
            }

            const block = document.createElement('div');
            block.className = 'block';
            block.style.width = 'auto';
            block.style.height = '70%';
            block.style.aspectRatio = '1';
            block.style.borderRadius = '100%';
            block.style.backgroundColor = '#EBF8EF';

            const button = document.createElement('button');
            button.type = 'submit';
            button.style = 'width: 100%; height: 100%;';
            button.value = types[i];
            button.name = 'filter_button';

            // block.onclick = function() { search_filter(types[i]); };
            // block.setAttribute('onclick', 'search_filter("' + types[i] + '");');

            // <p class="material-symbols-outlined color-contour2" style="font-size: 30px; margin: 0" onclick="show_filters()">menu</p>

            const symbol = document.createElement('p');
            symbol.className = 'material-symbols-outlined color-highlight';
            symbol.style = 'font-size: 30px; margin: 0';
            symbol.innerText = symbols[i];

            button.appendChild(symbol);
            block.appendChild(button);

            rows.at(-1).appendChild(block);
            i++;
        });

        rows.forEach(row => {
            new_element.appendChild(row);
        });

        box.appendChild(new_element);

        new_element.style.height = new_element.scrollHeight + 'px';

        setTimeout(() => {
            new_element.classList.add('show');
        }, 10);
    }
    else {
        // box.style.padding = "0";
        box.innerHTML = '';
    }
}