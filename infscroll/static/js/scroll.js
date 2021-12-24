/*
 * Make XMLHttpRequest compatible with old IEs.
 */
function createXHR( ) {
    try { return new XMLHttpRequest( ); } catch(e) {}
    try { return new ActiveXObject("Msxml2.XMLHTTP.6.0"); } catch (e) {}
    try { return new ActiveXObject("Msxml2.XMLHTTP.3.0"); } catch (e) {}
    try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {}
    try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {}
    return null; // no XHR support
}

/*
 * Fired when the user scrolls down.
 * When the visitor scrolled enough, starts to load more items from ajax.
 */
function scrollDown(ev) {
    // for Debug 
    // console.log('document.body.scrollHeight '+  document.body.scrollHeight + '\nwindow.innerHeight ' + window.innerHeight + '\ndocument.body.scrollTop '+ document.body.scrollTop+ '\ndocument.body.offsetHeight '+ document.body.offsetHeight+ '\nwindow.pageYOffset '+ window.pageYOffset);
    var half = parseInt(document.body.scrollHeight / 4);
    if (window.pageYOffset + window.innerHeight >= document.body.scrollHeight - half) {
        if (window.has_more == "True") {
            load_more();
        }
    }
    var sjmp = document.getElementById('scroll-jmp');
    if (sjmp && window.pageYOffset > 1500) {
        if (sjmp.style.display != 'block') {
            document.getElementById('scroll-jmp').style.display = 'block';
        }
    } else {
        if (sjmp.style.display != 'none') {
            document.getElementById('scroll-jmp').style.display = 'none';
        }
    }
    var ldmore = document.getElementById('a-load-more');
    if (ldmore !== null && ldmore.style.display != 'block') {
        document.getElementById('a-load-more').style.display = 'none';
    }
}
/*
 * Makes the ajax request and when its done, load the content to the 'div_name'
 */
function updt_from_url(url, div_name, callback) {
    var xmlhttp = new createXHR();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            if (typeof callback == "function") {
                callback(div_name);
            }
        }
    };
    xmlhttp.open("GET", url, async = true);
    xmlhttp.send();
}
/*
 * Prepare the environment to get more data and make the ajax call
 */
function load_more() {
    if (window.current_lap === undefined) {
        window.current_lap = 0;
        window.has_more = "True";
    }
    var load_more_div = document.getElementById('load_more');
    var div_name = 'load_more_' + window.current_lap + '_' + window.next_page;
    var element = document.getElementById(div_name);
    if (element === null) {
        element = document.createElement("div");
        element.setAttribute("id", div_name);
        element.innerHTML = '<i class="fa fa-spinner fa-spin" title="loading..."></i>';
        load_more_div.appendChild(element);
        // console.log('callback'+ window.current_pagination+' next_page '+ window.next_page+ ' has more '+ window.has_more );
        updt_from_url(window.more_url + '?' + window.extra_args + '&page=' + window.next_page, div_name, load_more_callback);
    }
    return false;
}
/*
 * Grabs information from the last call in order to prepare for the next call.
 */
function load_more_callback(div_name) {
    var div = document.getElementById(div_name);
    window.next_page = div.querySelector('#next_page').value;
    window.prev_page = div.querySelector('#prev_page').value;
    window.current_pagination = div.querySelector('#current_pagination').value;
    window.has_more = div.querySelector('#has_more').value;
    if (window.has_more != "True") {
        window.current_lap += 1;
        window.next_page = 0;
        window.has_more = "True";
    }
    if (typeof after_load_more === 'function') {
        after_load_more();
    }
    // console.log('current_pagination'+ window.current_pagination+' next_page '+ window.next_page+ ' has more '+ window.has_more );
}

/*
 * Scroll back to the top when we hit the UP button.
 */
function scrollToTop() {
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

/*
 * bind the onscroll event
 */
window.onscroll = scrollDown;
