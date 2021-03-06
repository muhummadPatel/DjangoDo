// on document ready, show the user all their lists
(function($){
  update_lists();
})(jQuery);


/******************** List related functions ********************/

// Get and display all lists for this user
function update_lists(){
  $("#user-list-names").empty();

  $.getJSON("/lists/", function(user_lists){
    $.each(user_lists, function(index, user_list){
      list_id = user_list.pk;
      list_name = user_list.fields.name;
      list_html = "<li class=\"collection-item\"><div><a id=\"listname_" + list_id + "\" href=\"#\">" + list_name + "</a><a id=\"deletelist_" + list_id + "\" href=\"#\" class=\"secondary-content\"><i class=\"material-icons md-18\">delete</i></a><div></li>";
      $("#user-list-names").append(list_html);
    });
  });
}

// Add a new list for this user
$("#new-list-form").on('submit', function(event){
  event.preventDefault();

  list_name = $("#todolist-name").val();
  $("#todolist-name").val("");
  $("label[for=\"todolist-name\"]").removeClass("active");

  data = { todolist_name: list_name };
  $.post("/lists/", data, function(){

    update_lists();
  }).fail(function(){

    alert("Sorry, an error occurred. :/");
  });
});

// Delete a list
$("#user-list-names").on("click", ".secondary-content", function(){
  event.preventDefault();

  active_list_id = $("[id^=active-list-name]").attr("id").match(/\d+/g) || [];
  list_id = $(this).attr("id").match(/\d+/g); // get the id of the list to be deleted
  if(list_id.length === 0){
    alert("Sorry, an error occurred. :/");
    return false;
  }else{
    list_id = list_id[0];
  }

  // POST to delete the specified list
  $.post("/lists/" + list_id + "/delete/", function(){
    update_lists();
    if(active_list_id.length !== 0 && list_id == active_list_id[0]){
      // we deleted the currently active list, or there was no active list
      // so reset the items card
      $("#list-items-prompt").removeClass("hide");
      $("#add-item-btn").addClass("hide");

      // set the collection header and append the list_id to the header id attr
      $("[id^=active-list-name]").html("Todo Items");
      $("[id^=active-list-name]").attr("id", "active-list-name");

      $("#list-items").empty(); //clear out old items
    }
  }).fail(function(){
    alert("Sorry, an error occurred. :/");
  });
});

// Make clicked list active and show items in that list
$("#user-list-names").on("click", ".collection-item a", function(){
  event.preventDefault();

  // make the selected list active
  $(".collection-item").removeClass("active");
  $(this).closest(".collection-item").addClass("active");

  // get and display the items in this list
  list_name = $(this).text();
  list_id = $(this).attr("id").match(/\d+/g);
  if(list_id.length === 0){
    return false;
  }else{
    list_id = list_id[0];
  }
  update_items(list_id, list_name);
});


/******************** Item related functions ********************/

// Get and display items in the active list
function update_items(list_id, list_name){
  show_all = $("#show-all-switch").is(":checked");
  $.getJSON("/lists/" + list_id + "/items/" , function(list_items){
    $("#list-items-prompt").addClass("hide");
    $("#add-item-btn").removeClass("hide");

    // set the collection header and append the list_id to the header id attr
    if(typeof list_name !== 'undefined' ){
      $("[id^=active-list-name]").html(list_name);
    }
    $("[id^=active-list-name]").attr("id", "active-list-name_" + list_id);

    $("#list-items").empty(); //clear out old items

    $.each(list_items, function(index, list_item){
      item_id = list_item.pk;
      item_text = list_item.fields.item_text;
      status = (list_item.fields.completed)? "checked": "";

      if(!list_item.fields.completed || show_all){
        cbox_id = "listitem_" + item_id;
        item_html = "<li class=\"collection-item\"><div><input id=\"" + cbox_id + "\" name=\"" + cbox_id + "\" type=\"checkbox\" " + status + "></input><label for=\"" + cbox_id + "\">" + item_text + "</label><a id=\"deleteitem_" + item_id + "\" href=\"#\" class=\"secondary-content\"><i class=\"material-icons md-18\">delete</i></a><div></li>";
        $("#list-items").append(item_html);
      }
    });
  });
}

// Add a new item to the active list
$("#new-item-form").on('submit', function(event){
  event.preventDefault();

  // get the form data and reset the form
  new_item_text = $("#todo-item-text").val();
  $("#todo-item-text").val("");
  $("label[for=\"todo-item-text\"]").removeClass("active");

  list_id = $("[id^=active-list-name]").attr("id").match(/\d+/g);
  if(list_id.length === 0){
    alert("Sorry, an error occurred. :/");
    return false;
  }else{
    list_id = list_id[0];
  }

  data = { item_text: new_item_text };
  $.post("/lists/" + list_id + "/items/", data, function(){
    update_items(list_id);
  }).fail(function(){
    alert("Sorry, an error occurred. :/");
  });
});

// Delete an item when the user clicks the trash can
$("#list-items").on("click", ".secondary-content", function(){
  event.preventDefault();

  // get the id of the item to be deleted and it's list
  list_id = $("[id^=active-list-name]").attr("id").match(/\d+/g);
  if(list_id.length === 0){
    alert("Sorry, an error occurred. :/");
    return false;
  }else{
    list_id = list_id[0];
  }
  item_id = $(this).attr("id").match(/\d+/g);
  if(item_id.length === 0){
    alert("Sorry, an error occurred. :/");
    return false;
  }else{
    item_id = item_id[0];
  }

  // POST to delete the specified list
  $.post("/lists/" + list_id + "/items/" + item_id + "/delete/", function(){
    update_items(list_id);
  }).fail(function(){
    alert("Sorry, an error occurred. :/");
  });
});

// Update item status when the user changes a checkbox
$("#list-items").on("change", "[id^=listitem]",function(){
  status = $(this).is(":checked");
  item_id = $(this).attr("id").match(/\d+/g);
  if(item_id.length === 0){
    alert("Sorry, an error occurred. :/");
    return false;
  }else{
    item_id = item_id[0];
  }

  data = { item_status: status};
  $.post("/lists/" + list_id + "/items/" + item_id + "/", data, function(){
    update_items(list_id);
  }).fail(function(){
    alert("Sorry, an error occurred. :/");
  });
});

// Toggle between showing all items or only showing completed items
$("#show-all-switch").on("change", function(){
  list_id = $("[id^=active-list-name]").attr("id").match(/\d+/g);
  if(list_id !== null){
    update_items(list_id[0]);
  }
});
