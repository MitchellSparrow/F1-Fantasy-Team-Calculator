
$(window).on('load', function(){ 
    $('#loading').hide();
});

function checkInp(){
  var x=document.forms["budget_form"]["budget"].value;
  if (isNaN(x)) 
  {
    alert("Your budget must be a number!");
    return false;
  }
  $('#loading').show();
}

$("form").submit(function (e) {
    var validationFailed = false;
    // validation
    if (!isNaN( $("#search").val())){
      if ( $("#search").val() == null || $("#search").val() == "") {
          validationFailed = true;
      } 

      if (validationFailed) {
          $('#loading').hide();
          alert('Please enter your budget as a number!');
          e.preventDefault();
          return false;
      }
    }

    
 }); 

 (function($) {
  var CheckboxDropdown = function(el) {
    var _this = this;
    this.isOpen = false;
    this.areAllChecked = false;
    this.$el = $(el);
    this.$label = this.$el.find('.dropdown-label');
    this.$checkAll = this.$el.find('[data-toggle="check-all"]').first();
    this.$inputs = this.$el.find('[type="checkbox"]');
    
    this.onCheckBox();
    
    this.$label.on('click', function(e) {
      e.preventDefault();
      _this.toggleOpen();
    });
    
    this.$checkAll.on('click', function(e) {
      e.preventDefault();
      _this.onCheckAll();
    });
    
    this.$inputs.on('change', function(e) {
      _this.onCheckBox();
    });
  };
  
  CheckboxDropdown.prototype.onCheckBox = function() {
    this.updateStatus();
  };
  
  CheckboxDropdown.prototype.updateStatus = function() {
    var checked = this.$el.find(':checked');
    
    this.areAllChecked = false;
    this.$checkAll.html('Check All');
    
    if(checked.length <= 0) {
      this.$label.html('Select Options');
    }
    // else if(checked.length === 1) {
    //   this.$label.html(checked.parent('label').text());
    // }
    else if(checked.length === this.$inputs.length) {
      this.$label.html('All Selected');
      this.areAllChecked = true;
      this.$checkAll.html('Uncheck All');
    }
    else {
      this.$label.html(checked.length + ' Selected');
    }
  };
  
  CheckboxDropdown.prototype.onCheckAll = function(checkAll) {
    if(!this.areAllChecked || checkAll) {
      this.areAllChecked = true;
      this.$checkAll.html('Uncheck All');
      this.$inputs.prop('checked', true);
    }
    else {
      this.areAllChecked = false;
      this.$checkAll.html('Check All');
      this.$inputs.prop('checked', false);
    }
    
    this.updateStatus();
  };
  
  CheckboxDropdown.prototype.toggleOpen = function(forceOpen) {
    var _this = this;
    
    if(!this.isOpen || forceOpen) {
       this.isOpen = true;
       this.$el.addClass('on');
      $(document).on('click', function(e) {
        if(!$(e.target).closest('[data-control]').length) {
         _this.toggleOpen();
        }
      });
    }
    else {
      this.isOpen = false;
      this.$el.removeClass('on');
      $(document).off('click');
    }
  };
  
  var checkboxesDropdowns = document.querySelectorAll('[data-control="checkbox-dropdown"]');
  for(var i = 0, length = checkboxesDropdowns.length; i < length; i++) {
    new CheckboxDropdown(checkboxesDropdowns[i]);
  }
})(jQuery);

$(document).ready(function(){
  $('#driver_bets_table tr.odds_row').each(function(){
      if (parseInt($(this).find(".price_rank").text(), 10) < parseInt($(this).find(".odds_rank").text(), 10)) {
          $(this).find(".price_rank").css('background-color','hsla(0, 100%, 50%, 0.4)');
      }else if (parseInt($(this).find(".price_rank").text(), 10) > parseInt($(this).find(".odds_rank").text(), 10)) {
        $(this).find(".price_rank").css('background-color','hsla(120,60%,70%,0.5)');
      }
      if (parseInt($(this).find(".points_rank").text(), 10) < parseInt($(this).find(".odds_rank").text(), 10)) {
        $(this).find(".points_rank").css('background-color','hsla(0, 100%, 50%, 0.4)');
        }else if (parseInt($(this).find(".points_rank").text(), 10) > parseInt($(this).find(".odds_rank").text(), 10)) {
          $(this).find(".points_rank").css('background-color','hsla(120,60%,70%,0.5)');
      }
  });

  $('#constructor_bets_table tr.odds_row').each(function(){
    if (parseInt($(this).find(".price_rank").text(), 10) < parseInt($(this).find(".odds_rank").text(), 10)) {
        $(this).find(".price_rank").css('background-color','hsla(0, 100%, 50%, 0.4)');
    }else if (parseInt($(this).find(".price_rank").text(), 10) > parseInt($(this).find(".odds_rank").text(), 10)) {
      $(this).find(".price_rank").css('background-color','hsla(120,60%,70%,0.5)');
    }
    if (parseInt($(this).find(".points_rank").text(), 10) < parseInt($(this).find(".odds_rank").text(), 10)) {
      $(this).find(".points_rank").css('background-color','hsla(0, 100%, 50%, 0.4)');
      }else if (parseInt($(this).find(".points_rank").text(), 10) > parseInt($(this).find(".odds_rank").text(), 10)) {
        $(this).find(".points_rank").css('background-color','hsla(120,60%,70%,0.5)');
    }
});

});

$(document).ready(function(){
  $('#btn-grand-prix-bets, #btn-championship-bets').click(function(){
      $('#btn-grand-prix-bets, #btn-championship-bets').removeClass('primary');
      $(this).addClass('primary');
      var selected = $(this).text();
      $(".gtr-200").hide();
      $('#' + selected.replace(/ /g,"_")).show();
  });
  
});



$(document).ready(function(){
  $('#btn-all, #btn-guardian, #btn-times, #btn-nyt, #btn-cityam, #btn-telegraph').click(function(){
      $('#btn-all, #btn-guardian, #btn-times, #btn-nyt, #btn-cityam, #btn-telegraph').removeClass('primary');
      $(this).addClass('primary');
      update_filtered_news();
  });
});


var divs;
    
$('.news_item').each(function(i){
  $(this).data('initial-index', i);
});


function update_filtered_news(){
  if(divs) {
    $(divs).appendTo('.news_board_items').each(function(){
          var oldIndex = $(this).data('initial-index');
          $('.news_item').eq(oldIndex).before(this);
      });
      divs = null;
  } 
 
  var input, filter, ul, li, a, i, txtValue;
  source_filter = $(".primary").text();
  //console.log(source_filter);
  input = document.getElementById('filter_news_text');
  filter = input.value.toUpperCase();
  ul = document.getElementById("news_table");
  li = ul.getElementsByTagName('tr');

  test = []

 
  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i];
    //console.log(a.getElementsByClassName("news_item_source")[0].textContent, source_filter);
    if(a.getElementsByClassName("news_item_source")[0].textContent == source_filter || source_filter == "All News"){
      
      txtValue = a.textContent || a.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
      } else {
        test.push(li[i]);
      }
    }else{
      test.push(li[i]);
    }
  }

  divs = $(test).detach();
}

$(document).keyup(function() { 
  update_filtered_news();
});







