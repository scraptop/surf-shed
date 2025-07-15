const CLASS_ACTIVE = 'btn-info';
const CLASS_DEACTIVE = 'btn-primary';

function changeTimeButtonClass(selectedButton) {
	toggleButton(selectedButton, "time-button" );
	prefix = "time-button";

  const consecutive = getConsecutiveActive(selectedButton, prefix) ;
	// if(consecutive.length == 0){return;}
	const firstInfo = getButtonInfo(consecutive[0], prefix);
	const lastInfo = getButtonInfo(consecutive[consecutive.length - 1], prefix);

	// update div with latest active
	updateInfoDisplay(firstInfo, lastInfo);

}


function getButtonInfo(button, prefix = 'prefix') {
  const match = button.id.match(new RegExp(`^${prefix}-(\\d+)-(\\d+)$`));
  if (!match) return null;
  const [ , colStr, rowStr ] = match;
  const timeDataInput = button.querySelector('input[name="time_data"]');
  const timeData = timeDataInput?.value;

  return {
    col: parseInt(colStr, 10),
    row: parseInt(rowStr, 10),
    start_time: timeData,
    idPrefix: prefix
  };
}

function isAdjacentToActive(button, prefix = 'prefix') {
  const info = getButtonInfo(button, prefix);
  if (!info) return false;

  const { col, row } = info;

  const prev = document.getElementById(`${prefix}-${col}-${row - 1}`);
  const next = document.getElementById(`${prefix}-${col}-${row + 1}`);

  return (prev && prev.classList.contains(CLASS_ACTIVE)) ||
         (next && next.classList.contains(CLASS_ACTIVE));
}

function getConsecutiveActive(button, prefix = 'prefix') {
  const info = getButtonInfo(button, prefix);
  if (!info) return [];

  const { col, row } = info;
  const activeButtons = [];

	// check self
   const el = document.getElementById(`${prefix}-${col}-${row}`);
	if (el && el.classList.contains(CLASS_ACTIVE)) {
		activeButtons.unshift(el);
	}

  // Look up
  let r = row - 1;
  while (true) {
    const el = document.getElementById(`${prefix}-${col}-${r}`);
    if (el && el.classList.contains(CLASS_ACTIVE)) {
      activeButtons.unshift(el);
      r--;
    } else break;
  }

  // Look down
  r = row + 1;
  while (true) {
    const el = document.getElementById(`${prefix}-${col}-${r}`);
    if (el && el.classList.contains(CLASS_ACTIVE)) {
      activeButtons.push(el);
      r++;
    } else break;
  }

  return activeButtons;
}

function getConsecutiveActiveIncludingSelectedButton(button, prefix = 'prefix') {
  const info = getButtonInfo(button, prefix);
  if (!info) return [];

  const { col, row } = info;
  const activeButtons = [button];

  // Look up
  let r = row - 1;
  while (true) {
    const el = document.getElementById(`${prefix}-${col}-${r}`);
    if (el && el.classList.contains(CLASS_ACTIVE)) {
      activeButtons.unshift(el);
      r--;
    } else break;
  }

  // Look down
  r = row + 1;
  while (true) {
    const el = document.getElementById(`${prefix}-${col}-${r}`);
    if (el && el.classList.contains(CLASS_ACTIVE)) {
      activeButtons.push(el);
      r++;
    } else break;
  }

  return activeButtons;
}

function deactivateButton(button) {
  button.classList.remove(CLASS_ACTIVE);
  button.classList.add(CLASS_DEACTIVE);
}

function deactivateAll(prefix = 'prefix') {
  document.querySelectorAll(`button[id^="${prefix}-"].${CLASS_ACTIVE}`)
    .forEach(btn => deactivateButton(btn));
}

function activateButton(button) {
  button.classList.remove(CLASS_DEACTIVE);
  button.classList.add(CLASS_ACTIVE);
}

function insertInputElementToDiv(div, inputId, inputValue, name){

  // Try to find the existing input by name
  // let hiddenInput = div.querySelector(`input[type="hidden"][id="${inputId}"]`);
  let hiddenInput = div.querySelector(`input[id="${inputId}"]`);

  if (hiddenInput) {
    // If it exists, just update the value
    hiddenInput.value = inputValue;
  } else {
    // Otherwise, create and append the hidden input
    hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.id = inputId;
    hiddenInput.name = inputId;
    hiddenInput.value = inputValue;
    div.appendChild(hiddenInput);
  }

}

function updateInfoDisplay(firstInfo, lastInfo) {
  infoDiv = document.getElementById("bosse");
  if (!infoDiv || !firstInfo || !lastInfo) return;

  insertInputElementToDiv(infoDiv, "selection_start_time", firstInfo.start_time, "time_data_start");
  insertInputElementToDiv(infoDiv, "selection_end_time", lastInfo.start_time, "time_data_end");

  // Apply only if you need debug
  // const debugDiv = document.createElement('div');
  // debugDiv.textContent =
  //   `Active Range: Column ${firstInfo.col},
  //    Rows ${firstInfo.row} to ${lastInfo.row}.
  //    TimeStart: ${firstInfo.start_time} to ${lastInfo.start_time} `;
  // infoDiv.appendChild(debugDiv);

}

function toggleButton(button, prefix = 'prefix') {
  if (!button || !button.id) return;

  const MAX_ACTIVE = 5;
  const consecutive = getConsecutiveActiveIncludingSelectedButton(button, prefix);
	const info = getButtonInfo(button, prefix);
	const firstInfo = getButtonInfo(consecutive[0], prefix);
	const lastInfo = getButtonInfo(consecutive[consecutive.length - 1], prefix);

  if (button.classList.contains(CLASS_ACTIVE)) {
    if ((info.row == lastInfo.row) || (info.row == firstInfo.row)) {

        deactivateButton(button);
        return;
      }
  }

  const adjacent = isAdjacentToActive(button, prefix);

  if (!adjacent) {
    deactivateAll(prefix);
    activateButton(button);
    return;
  }



  if (consecutive.length < MAX_ACTIVE) {
    activateButton(button);
  } else if (consecutive.length === MAX_ACTIVE) {

    if (!info || !firstInfo || !lastInfo) return;

    if (info.row == lastInfo.row) {
      // Clicked below the current group → remove top
			console.log("Clicked below the current group → remove top");
      deactivateButton(consecutive[0]);

    } else if (info.row == firstInfo.row) {
      // Clicked above the group → remove bottom
			console.log("Clicked above the group → remove bottom");
      deactivateButton(consecutive[MAX_ACTIVE-1]);

    } else {
      // Clicked in the middle → invalid (won't increase total)
      //alert("Can't activate more than 3 in a row. h'st");
			console.log("Can't activate more than 3 in a row.");
      return;
    }

    activateButton(button);
  } else {
    // Just in case (shouldn't happen)
    alert("Too many consecutive active buttons.");
  }
}
