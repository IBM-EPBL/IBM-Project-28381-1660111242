function getbmrvalue() {

  var age = document.getElementById('age').value;
  var gender = document.querySelector('input[name="customRadioInline1"]:checked');
  var weight= document.getElementById('weight').value;
  var height= document.getElementById('height').value;
  var activity = document.getElementById('list').value;
  var height_status = false;
  var weight_status = false;
  var age_status = false;
  var newbmrvalue = "";


  if(height === "" || isNaN(height) || (height<=0))
  {
      document.getElementById('height_error').innerHTML = "Please provide a valid height";
  }
  else{
      document.getElementById('height_error').innerHTML = "";
      height_status = true ; 
  }
  if(weight === "" || isNaN(weight) || (weight<=0))
  {
      document.getElementById('weight_error').innerHTML = "Please provide a valid weight";
  }
  else{
      document.getElementById('weight_error').innerHTML = "";
      weight_status = true ; 
  }
  if(age === "" || isNaN(age) || (age<10) || (age>80) )
  {
      document.getElementById('age_error').innerHTML = "Please provide a valid age";
  }
  else{
      document.getElementById('age_error').innerHTML = "";
      age_status = true ; 
  }
  
  if(height_status && weight_status && age_status && gender.id === 'male')
  {
    if(activity === "1") 
    {
      newbmrvalue = 1.2 * (66.5 + (13.75 * parseFloat(weight)) + (5.003 * parseFloat(height)) - (6.755 * parseFloat(age)));
    }
    else if(activity === "2") 
    {
      newbmrvalue = 1.375 * (66.5 + (13.75 * parseFloat(weight)) + (5.003 * parseFloat(height)) - (6.755 * parseFloat(age)));
    }
    else if ( activity === "3") 
    {
      newbmrvalue = 1.55 * (66.5 + (13.75 * parseFloat(weight)) + (5.003 * parseFloat(height)) - (6.755 * parseFloat(age)));
    }
    else if( activity === "4") 
    {
      newbmrvalue = 1.725 * (66.5 + (13.75 * parseFloat(weight)) + (5.003 * parseFloat(height)) - (6.755 * parseFloat(age)));
    } 
    else
    {
      newbmrvalue = 1.9 * (66.5 + (13.75 * parseFloat(weight)) + (5.003 * parseFloat(height)) - (6.755 * parseFloat(age)));
    }
  }
  

  if(height_status && weight_status && age_status && gender.id === 'female')
  {
    if( activity === "1") 
    {
      newbmrvalue = 1.2 * (655 + (9.563 * parseFloat(weight)) + (1.850 * parseFloat(height)) - (4.676 * parseFloat(age)));
    }
    else if(activity === "2") 
    {
      newbmrvalue = 1.375 * (655 + (9.563 * parseFloat(weight)) + (1.850 * parseFloat(height)) - (4.676 * parseFloat(age)));
    }  
    else if(activity === "3") {
      newbmrvalue = 1.55 * (655 + (9.563 * parseFloat(weight)) + (1.850 * parseFloat(height)) - (4.676 * parseFloat(age)));
    }
    else if( activity === "4") {
      newbmrvalue = 1.725* (655 + (9.563 * parseFloat(weight)) + (1.850 * parseFloat(height)) - (4.676 * parseFloat(age)));
    }
    else {
      newbmrvalue = 1.9 * (655 + (9.563 * parseFloat(weight)) + (1.850 * parseFloat(height)) - (4.676 * parseFloat(age)));
    } 
  }

  newbmrvalue = newbmrvalue.toFixed(2);
  document.getElementById('result').innerHTML = "BMR Value: " + newbmrvalue;


}



