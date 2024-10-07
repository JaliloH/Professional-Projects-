// SOURCE: https://www.w3schools.com/howto/howto_js_filter_lists.asp

var overList = false;

function myFunction() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  li = ul.getElementsByTagName('li');

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
};

function showList() {
    var ul = document.getElementById("myUL");
    ul.removeAttribute("hidden");
}

function hideList() {
    if (!overList) {
        var ul = document.getElementById("myUL");
        ul.setAttribute("hidden", true);
    }
}

function enterList() {
    overList = true;
}

function leaveList() {
    overList = false;
    hideList();
}


// async function filterBrowse(id) {
//     if (id == 1) {
//         const url = "http://localhost:5117/feed/bars";
//         const request = {
//             method: "GET",
//             headers: { 
//                 "Content-Type": "application/json"
//             }
//         };
//         const response = await fetch(url, request);
//         if (response.ok) {
//             location.reload()
//             return;
//         }
//     } else if (id == 2) {
//         const url = "http://localhost:5117/feed/beauty";
//         const request = {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json"
//             }
//         };
//         const response = await fetch(url, request);
//         if (response.ok) {
//             console.log(response)
//             location.reload()
//             return;
//         }
    
//     }else {
//         console.log("Invalid ordering.")
//         return -1;
        
//     }
//     console.log("it worked")
//     return;
// };

// // document.addEventListener("DOMContentLoaded", function() {
// //     let by_bars = document.getElementById("filter1");
// //     let by_beauty = document.getElementById("filter2");
// //     let by_cafes = document.getElementById("filter3");
// //     let by_edible = document.getElementById("filter4");
// //     let by_restaurants = document.getElementById("filter5");
// //     let by_stores = document.getElementById("filter6");
// //     let by_stars_asc = document.getElementById("filter7");
// //     let by_stars_desc = document.getElementById("filter8");
// //     let five_stars = document.getElementById("filter9");
// //     let four_stars = document.getElementById("filter10");
// //     let three_stars = document.getElementById("filter11");
// //     let two_stars = document.getElementById("filter12");
// //     let one_star = document.getElementById("filter13");
// // });