let nav = "nav-"; // prefix of button elements
let top_button = "about"; // top of the page
let sections = ["contacts", "academic", "teaching", "publications"]; // other sections

let navButtons = [nav + top_button, ...sections.map(section => nav + section)];

let lastClicked = Date.now(); // record the time when the flag is set
const TIME_THRESHOLD = 100; // milliseconds

const sizeQuery = window.matchMedia("(max-width: 860px)"); 

function setAllToNormal() {
  for (let i = 0; i < navButtons.length; i++) {
    document.getElementById(navButtons[i]).style.fontWeight =  "normal";
  }
}

function onlyThisBold(nav_button) {
  setAllToNormal();
  document.getElementById(nav_button).style.fontWeight = 'bold';
}

for (let i = 0; i < navButtons.length; i++) {
  document.getElementById(navButtons[i]).onclick = function(){
    onlyThisBold(navButtons[i]);
    lastClicked = Date.now();
  };
}

function handleResize() {
  if (sizeQuery.matches) { // if we are in "phone mode", set everything to normal
    setAllToNormal();
  }
  else { // else, pretend we just scrolled
    handleScroll();
  } 
} 

window.addEventListener('resize', () => {
  setTimeout(() => {
    handleResize();
  }, TIME_THRESHOLD);
});

function handleScroll() { 

  if (Date.now() - lastClicked <= TIME_THRESHOLD) { // if we just clicked on a button, do nothing
    return;
  }

  if (sizeQuery.matches) { // if we are on the phone, set all to normal and abort
    setAllToNormal();
    return;
  }

  //otherwise
  if (getVerticalScrollPercentage(document.body) === 0) { // if we are on top
    onlyThisBold(nav+top_button);
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

// When the page is loaded and seen,
document.addEventListener("DOMContentLoaded", () => {
  requestAnimationFrame(() => {
    // if we are not on the phone, set bold initially to the section we are at
    if (!sizeQuery.matches) {
      const hashFragment = window.location.hash.substring(1); // Removes the "#"
      // If hash is empty, do something with "about"
      onlyThisBold(nav+(hashFragment === "" ? top_button : hashFragment));
    }
  });
});