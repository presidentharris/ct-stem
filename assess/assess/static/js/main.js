
var curr_page = 0;
var page_count = 1;
var page_width = 770;


//-----------------------------------------------------------------------------
// called from body.onload
//-----------------------------------------------------------------------------
function startup() {
   var options = document.querySelectorAll(".check-all li");
   for (var i=0; i<options.length; i++) {
      var opt = options[i];
      opt.onclick = select;
   }
   
   //----------------------------------------------
   // Set up the radio-button selectors
   //----------------------------------------------
   options = document.querySelectorAll(".check-one li, .likert li");
   for (var i=0; i<options.length; i++) {
      options[i].onclick = selectOne;
   }
   
   
   
   //----------------------------------------------
   // Start with all pages invisible but spaced correctly
   //----------------------------------------------
   var pages = document.querySelectorAll(".page");
   for (var i=0; i<pages.length; i++) {
      var page = pages[i];
      page.id = "page" + i;
      page.style.left = (page_width * i) + "px";
   }
   page_count = pages.length;
   
   var hash = parent.location.hash;
   if (hash && hash.indexOf('#p') == 0) {
      gotoPage(parseInt(hash.substring(2)));
   } else {
      gotoPage(1);
   }

   
   //----------------------------------------------
   // Likert tables
   //----------------------------------------------
   var sets = document.querySelectorAll("table.likert tr");
   for (var i=0; i<sets.length; i++) {
      var options = sets[i].querySelectorAll("td");
      sets[i].setAttribute("id", "likert" + i);
      for (var j=0; j<options.length; j++) {
         var opt = options[j];
         if (!opt.classList.contains("prompt")) {
            opt.setAttribute("group", "likert" + i);
            opt.setAttribute("value", j);
            opt.onclick = function(e) {
               var group = document.querySelectorAll("tr#" + this.getAttribute("group") + " td");
               for (var i=0; i<group.length; i++) {
                  group[i].classList.remove("selected");
               }
               this.classList.add("selected");
            };
         }
      }
   }
}


//-----------------------------------------------------------------------------
// select one radio button from a list (onclick callback)
//-----------------------------------------------------------------------------
function selectOne(e) {
   var pnode = this.parentNode;
   var children = pnode.childNodes;
   for (var i=0; i<children.length; i++) {
      if (children[i] == this) {
         children[i].classList.add("selected");
      } else if (children[i].nodeName == "LI") {
         children[i].classList.remove("selected");
      }
   }
}


//-----------------------------------------------------------------------------
// Select a checkbox (onclick callback)
//-----------------------------------------------------------------------------
function select(e) {
   this.classList.toggle("selected");
}


//-----------------------------------------------------------------------------
// move to an arbitrary page (1 is the first page)
//-----------------------------------------------------------------------------
function gotoPage(p) {
   if (p > 0 && p <= page_count) {
      
      //-----------------------------------------------------
      // add the page number to the page hash to come back to
      // this page if the browser window is reloaded
      //-----------------------------------------------------
      parent.location.hash = "p" + p; 
      curr_page = p - 1;

      //-----------------------------------------------------
      // Set the page number at the bottom of the screen
      //-----------------------------------------------------
      setHtmlText("page-number", "Page " + p + " of " + page_count);

      //-----------------------------------------------------
      // Update the left margin for all pages. The CSS rule
      // for pages includes an animated transition on the left
      // margin property
      //-----------------------------------------------------
      var pages = document.querySelectorAll(".page");
      for (var i=0; i<pages.length; i++) {
         var page = pages[i];
         page.style.left = (page_width * (i - curr_page)) + "px";
         if (curr_page == i) {
            page.style.visibility = 'visible';

            var footer = document.getElementById("footer");
            if (footer) {
               footer.style.marginTop = page.clientHeight + "px";
            }
         } 
      }
   }
}


//-----------------------------------------------------------------------------
// Utility function for setting innerHtml
//-----------------------------------------------------------------------------
function setHtmlText(id, text) {
   var el = document.getElementById(id);
   if (el) el.innerHTML = text;
}


//-----------------------------------------------------------------------------
// Utility function for setting opacity
//-----------------------------------------------------------------------------
function setHtmlOpacity(id, opacity) {
   var el = document.getElementById(id);
   if (el) el.style.opacity = opacity;
}


//-----------------------------------------------------------------------------
// Utility function for setting the visibility status
//-----------------------------------------------------------------------------
function setHtmlVisibility(id, visible) {
   var el = document.getElementById(id);
   if (el) el.style.visibility = (visible) ? 'visible' : 'hidden';
}


//-----------------------------------------------------------------------------
// Utility function for enabling / disabling a button
//-----------------------------------------------------------------------------
function setHtmlEnabled(id, enabled) {
   var el = document.getElementById(id);
   if (el) {
      if (enabled) {
         el.classList.remove('disabled');
         el.disabled = false;
      } else {
         el.classList.add('disabled');
         el.disabled = true;
      }
   }
}



//-----------------------------------------------------------------------------
// go forward one page
//-----------------------------------------------------------------------------
function nextPage() {
   gotoPage(curr_page + 2);
   setHtmlOpacity("status", 1);
   window.setTimeout(function () { setHtmlOpacity("status", 0); }, 1000);   
}


//-----------------------------------------------------------------------------
// go back one page
//-----------------------------------------------------------------------------
function backPage() {
   gotoPage(curr_page);
   setHtmlOpacity("status", 1);
   window.setTimeout(function () { setHtmlOpacity("status", 0); }, 1000);   
}
