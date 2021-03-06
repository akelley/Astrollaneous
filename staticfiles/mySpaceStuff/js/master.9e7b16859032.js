function openTab(evt, tabName) {
  var tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tab-content");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  truncateText();
}

function truncateText() {
  $('.nasa-description-container').each(function () {
    var maxheight = 100;
    var text = $(this);
  
    if (text.height() > maxheight){
      text.css({ 'overflow': 'hidden','height': maxheight + 'px' });
  
      var link = $('<a href="#">Show More</a>');
      var linkDiv = $('<div></div>');
      linkDiv.append(link);
      $(this).after(linkDiv);
  
      link.click(function (event) {
        event.preventDefault();
  
        if (text.height() > maxheight) {
            $(this).html("Show More");
            text.css('height', maxheight + 'px');
        } else {
            $(this).html("Show Less");
            text.css('height', 'auto');
        }
      });
    }
  });
}

$(document).ready(function() {
  $('#nasa-submit').on('click', function() {   
    if ($('.nasa-search-input').val()) {
      $('.nasa-main-content').css('display', 'none');
      $('#loader-container').css('display', 'block');
    }
  });
});