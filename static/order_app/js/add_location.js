  
    // Get the modal
  var modal = document.getElementById("myModal");
  var modal2 = document.getElementById("myModal2");
  
  // Get the button that opens the modal
  var btn = document.getElementById("myBtn");
  var btn2 = document.getElementById("myBtn2");
  
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  var span2 = document.getElementsByClassName("close2")[0];

  let choses = document.getElementById('choses');
  let choses2 = document.getElementById('choses2');
  let item = JSON.parse(document.getElementById('item').textContent);
  let inputs = document.getElementsByTagName('input');
  let id_upload_file_if_any = document.getElementById('id_upload_file_if_any');


  // get form data in variables to save it to local storages

  let site_name = document.getElementById('id_site_name');
  let siteadd = document.getElementById('category');
  let schudule_date = document.getElementById('id_schudule_date');
  let Time = document.getElementById('id_Time');
  let description = document.getElementById('id_description');
  let upload_file_if_any = document.getElementById('id_upload_file_if_any');
  let extra_note = document.getElementById('id_extra_note');

  let submit_main_form = document.getElementById('submit_main_form');


  window.addEventListener('load', function() {

    if (localStorage.getItem('site_name') != ""){
      site_name.value = localStorage.getItem('site_name');
    }

    if (localStorage.getItem('siteadd') != ""){
      siteadd.value = localStorage.getItem('siteadd');
    }

    if (localStorage.getItem('contact_person') != ""){
      contact_person.value = localStorage.getItem('contact_person');
    }

    if (localStorage.getItem('schudule_date') != ""){
      schudule_date.value = localStorage.getItem('schudule_date');
    }

    if (localStorage.getItem('Time') != ""){
      Time.value = localStorage.getItem('Time');
    }

    if (localStorage.getItem('description') != ""){
      description.value = localStorage.getItem('description');
    }

    if (localStorage.getItem('extra_note') != ""){
      extra_note.value = localStorage.getItem('extra_note');
    }
  }, false);


  
  // When the user clicks on the button, open the modal
  btn.onclick = function() {
    console.log('click on btn')
    modal.style.display = "block";
  }

  btn2.onclick = function() {
    console.log('click on btn')
    modal2.style.display = "block";
  }
  
  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }
  
  span2.onclick = function() {
    modal2.style.display = "none";
  }
  

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }

  window.onclick = function(event) {
    if (event.target == modal) {
      modal2.style.display = "none";
    }
  };
  
  id_upload_file_if_any.setAttribute("multiple","true")


  function changFanc(){
  
    localStorage.setItem('site_name',site_name.value);
    localStorage.setItem('siteadd',siteadd.value);
    localStorage.setItem('contact_person',contact_person.value);
    localStorage.setItem('schudule_date',schudule_date.value);
    localStorage.setItem('Time',Time.value);
    localStorage.setItem('description',description.value);
    localStorage.setItem('upload_file_if_any',upload_file_if_any.value);
    localStorage.setItem('extra_note',extra_note.value);

  }

  submit_main_form.addEventListener('click', function(){
    localStorage.setItem('site_name','');
    localStorage.setItem('siteadd','');
    localStorage.setItem('contact_person','');
    localStorage.setItem('schudule_date','');
    localStorage.setItem('Time','');
    localStorage.setItem('description','');
    localStorage.setItem('upload_file_if_any','');
    localStorage.setItem('extra_note','');
  })
  