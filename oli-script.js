let nav = "nav-"; // prefix of button elements
let top_button = "about"; // top of the page
let sections = ["contacts", "academic", "teaching", "publications"]; // other sections
let justclicked = false;

const sizeQuery = window.matchMedia("(max-width: 860px)"); 

// button clicks!

document.getElementById(nav+top_button).onclick = function() {
  justclicked = true;
  document.getElementById(nav+top_button).style.fontWeight = 'bold';
  for (let i = 0; i < sections.length; i++) {
    document.getElementById(nav+sections[i]).style.fontWeight = "normal";
  }
}

for (let i = 0; i < sections.length; i++) {
  document.getElementById(nav+sections[i]).onclick = function(){
    justclicked = true;
    document.getElementById(nav+top_button).style.fontWeight = 'normal';
    for (let j = 0; j < sections.length; j++) {
      document.getElementById(nav+sections[j]).style.fontWeight = i === j ? "bold" : "normal";
    }
  }
}

//

function handleResize() {
  if (sizeQuery.matches) { // if we are in "phone mode", set everything to normal
    document.getElementById(nav+top_button).style.fontWeight = 'normal';
    for (let i = 0; i < sections.length; i++) {
      document.getElementById(nav+sections[i]).style.fontWeight = 'normal';
    }
  }
  else { handleScroll(); } // otherwise, pretend we just scrolled
} 

window.onresize = handleResize;

function handleScroll() { 

  if (sizeQuery.matches) { // if we are in "phone mode", abort
    return;
  } 

  if (justclicked) { // if we are in "phone mode", abort
    justclicked = false;
    return;
  } 

  //otherwise
  if (getVerticalScrollPercentage(document.body) === 0) { // if we are on top
    document.getElementById(nav+top_button).style.fontWeight = 'bold'; // set about to bold
    for (let i = 0; i < sections.length; i++) {
      document.getElementById(nav+sections[i]).style.fontWeight = 'normal'; // rest to normal
    }
  } else { // else, scroll sections from bottom to top; the last section that is 
    // on view (thus, the first we encouter):
    // we set that to bold
    // set rest to normal
    // stop
    for (let i = 0; i < sections.length; i++) {
      if (isElementInViewport(document.getElementById(sections[i]))) {
        document.getElementById(nav+top_button).style.fontWeight = 'normal';
        for (let j = 0; j < sections.length; j++) {
          document.getElementById(nav+sections[j]).style.fontWeight = i === j ? "bold" : "normal";
        }
        break;
      }
    }
  }
}

document.onscroll = handleScroll;

function isElementInViewport (el) { //is element visible?

    // Special bonus for those using jQuery
    if (typeof jQuery === "function" && el instanceof jQuery) {
        el = el[0];
    }

    var rect = el.getBoundingClientRect();

    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /* or $(window).height() */
        rect.right <= (window.innerWidth || document.documentElement.clientWidth) /* or $(window).width() */
    );
}

function getVerticalScrollPercentage(elm) { // scroll percentage of element
  var p = elm.parentNode;
  return (elm.scrollTop || p.scrollTop) / (p.scrollHeight - p.clientHeight) * 100;
}
