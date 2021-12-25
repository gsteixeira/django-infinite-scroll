/*
 * The InfiniteScroll object manages the data for pagination.
 */
class InfiniteScroll {
    more_url:string;
    extra_args:string;
    next_page:string;
    prev_page:string;
    has_more:boolean;
    keep_loading:boolean;
    current_lap:number;
    
    constructor() {
        this.current_lap = 0;
        this.keep_loading = false;
        this.more_url = "";
        this.prev_page = "";
        this.next_page = "";
        this.extra_args = "";
        this.has_more = false;
    }

    /*
     * set the initial parameters
     */
    setUp(url:string, prev:string, next:string,
          has_more:string, extra_args:string) {
        this.current_lap = 0;
        this.more_url = url;
        this.prev_page = prev;
        this.next_page = next;
        this.has_more = (has_more === "True");
        this.keep_loading = this.has_more;
        this.extra_args = extra_args;
    }
    
    /*
    * Prepare the environment to get more data and make the ajax call
    */
    load_more() {
        if (!this.keep_loading) {
            return false;
        }
        let load_more_div = document.getElementById('load_more');
        let div_name = 'load_more_' + this.current_lap + '_' + this.next_page;
        let element = document.getElementById(div_name);
        if (element === null && load_more_div !== null && div_name !== null) {
            element = document.createElement("div");
            element.setAttribute("id", div_name);
            element.innerHTML = '<i class="fa fa-spinner fa-spin" title="loading..."></i>';
            load_more_div.appendChild(element);
            let url = this.more_url + '?' + this.extra_args + '&page=' + this.next_page;
            updt_from_url(url, div_name, load_more_callback);
        }
        return true;
    }
}

var scroller = new InfiniteScroll();

/*
 * Fired when the user scrolls down.
 * When the visitor scrolled enough, starts to load more items from ajax.
 */
function scrollDown(ev:Object) {
    let half = Math.floor(document.body.scrollHeight / 4);
    if (window.pageYOffset + window.innerHeight >= document.body.scrollHeight - half) {
        scroller.load_more();
    }
    let sjmp = document.getElementById('scroll-jmp');
    if (sjmp !== null && window.pageYOffset > 1500) {
        if (sjmp.style.display != 'block') {
            document.getElementById('scroll-jmp').style.display = 'block';
        }
    } else if (sjmp !== null && sjmp.style.display != 'none') {
        document.getElementById('scroll-jmp').style.display = 'none';
    }
    let ldmore = document.getElementById('a-load-more');
    if (ldmore !== null && ldmore.style.display != 'block') {
        document.getElementById('a-load-more').style.display = 'none';
    }
}

/*
 * Makes the ajax request and when its done, load the content to the 'div_name'
 */
function updt_from_url(url:string, div_name:string, callback:Function) {
    let xmlhttp = createXHR();
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById(div_name).innerHTML = xmlhttp.responseText;
            if (typeof callback == "function") {
                callback(div_name);
            }
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

/*
 * Grabs information from the last call in order to prepare for the next call.
 */
function load_more_callback(div_name:string) {
    let div = document.getElementById(div_name);
    if (div === null) {
        return
    }
    scroller.next_page = (<HTMLInputElement>div.querySelector('#next_page')).value;
    scroller.prev_page = (<HTMLInputElement>div.querySelector('#prev_page')).value;
    scroller.has_more = ((<HTMLInputElement>div.querySelector('#has_more')).value === "True");
    scroller.keep_loading = ((<HTMLInputElement>div.querySelector('#keep_loading')).value === "True");
    if (!scroller.has_more) {
        scroller.current_lap += 1;
        scroller.next_page = "0";
    }
    let after_load_more : Function | undefined;
    if (after_load_more !== undefined) {
        after_load_more()
    }
}

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
