var numberOfGrains = 1;
var numberOfHops = 1;
var numberOfOther = 1;

// Functions to allow the user to add custom amount of ingredients

function addGrain() {
  //Increment the number of grains
  numberOfGrains++;
  //Prepare the label/name/id for this new input
  var grainLabel = "grain" + String(numberOfGrains);
  //Get the template form and clone it
  var templateDiv = document.getElementById("template-grain");
  var newDiv = templateDiv.cloneNode(true);
  //Update the ids, names and labels of the new div
  newDiv.id = grainLabel;
  var divChildren = newDiv.children;
  divChildren[0].setAttribute("for", grainLabel);
  divChildren[1].setAttribute("name", grainLabel);
  divChildren[1].setAttribute("id", grainLabel);
  divChildren[2].setAttribute("for", grainLabel + "-qty");
  divChildren[3].setAttribute("name", grainLabel + "-qty");
  divChildren[3].setAttribute("id", grainLabel + "-qty");
  //Add the new div to the form
  document.getElementById("form-grains").appendChild(newDiv);
  //Update the number of grains in the form's hidden input
  document.getElementById("grains-num").setAttribute("value", numberOfGrains);
}

function addHop() {
  //Increment the number of hops
  numberOfHops++;
  //Prepare the label/name/id for this new input
  var hopLabel = "hops" + String(numberOfHops);
  //Get the template form and clone it
  var templateDiv = document.getElementById("template-hops");
  var newDiv = templateDiv.cloneNode(true);
  //Update the ids, names and labels of the new div
  newDiv.id = hopLabel;
  var divChildren = newDiv.children;
  divChildren[0].setAttribute("for", hopLabel);
  divChildren[1].setAttribute("name", hopLabel);
  divChildren[1].setAttribute("id", hopLabel);
  divChildren[2].setAttribute("for", hopLabel + "-qty");
  divChildren[3].setAttribute("name", hopLabel + "-qty");
  divChildren[3].setAttribute("id", hopLabel + "-qty");
  divChildren[5].setAttribute("name", hopLabel + "-use");
  divChildren[6].setAttribute("for", hopLabel + "-time");
  divChildren[7].setAttribute("name", hopLabel + "-time");
  divChildren[7].setAttribute("id", hopLabel + "-time");
  //Add the new div to the form
  document.getElementById("form-hops").appendChild(newDiv);
  //Update the number of hops in the form's hidden input
  document.getElementById("hops-num").setAttribute("value", numberOfHops);
}

function addOther() {
  //Increment the number of other ingredients
  numberOfOther++;
  //Prepare the label/name/id for this new input
  var otherLabel = "other" + String(numberOfOther);
  //Get the template form and clone it
  var templateDiv = document.getElementById("template-other");
  var newDiv = templateDiv.cloneNode(true);
  //Update the ids, names and labels of the new div
  newDiv.id = otherLabel;
  var divChildren = newDiv.children;
  divChildren[0].setAttribute("for", otherLabel);
  divChildren[1].setAttribute("name", otherLabel);
  divChildren[1].setAttribute("id", otherLabel);
  divChildren[2].setAttribute("for", otherLabel + "-qty");
  divChildren[3].setAttribute("name", otherLabel + "-qty");
  divChildren[3].setAttribute("id", otherLabel + "-qty");
  divChildren[5].setAttribute("for", otherLabel + "-details");
  divChildren[6].setAttribute("name", otherLabel + "-details");
  divChildren[6].setAttribute("id", otherLabel + "-details");
  //Add the new div to the form
  document.getElementById("form-other").appendChild(newDiv);
  //Update the number of other ingredients in the form's hidden input
  document.getElementById("other-num").setAttribute("value", numberOfOther);
}

// Functions to allow the user to remove ingredients

function removeGrain() {
  //If the number of grain is > 1 remove the latest grain input form
  if (numberOfGrains > 1) {
    var divId = "grain" + String(numberOfGrains);
    var elem = document.getElementById(divId);
    elem.parentNode.removeChild(elem);
    // Decrement numberOfGrains
    numberOfGrains--;
    //Update the number of grains in the form's hidden input
    document.getElementById("grains-num").setAttribute("value", numberOfGrains);
  }
}

function removeHop() {
  //If the number of grain is > 1 remove the latest grain input form
  if (numberOfHops > 1) {
    var divId = "hops" + String(numberOfHops);
    var elem = document.getElementById(divId);
    elem.parentNode.removeChild(elem);
    // Decrement numberOfGrains
    numberOfHops--;
    //Update the number of hops in the form's hidden input
    document.getElementById("hops-num").setAttribute("value", numberOfHops);
  }
}

function removeOther() {
  //If the number of grain is > 1 remove the latest grain input form
  if (numberOfOther > 1) {
    var divId = "other" + String(numberOfOther);
    var elem = document.getElementById(divId);
    elem.parentNode.removeChild(elem);
    // Decrement numberOfGrains
    numberOfOther--;
    //Update the number of other ingredients in the form's hidden input
    document.getElementById("other-num").setAttribute("value", numberOfOther);
  }
}
