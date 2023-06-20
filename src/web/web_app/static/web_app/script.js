const ul = document.querySelector("ul"),
input = ul.querySelector("input");

let tags = [];

function removeTags() {
    ul.querySelectorAll("li").forEach(li => li.remove());
}

function createTags() {
    let reversedTags = tags.slice().reverse()
    reversedTags.forEach(tag => {
        let liTag = `<li onclick="removeTag(this, '${tag}')">${tag}</li>`;
        // insert before the input textbox
        ul.insertAdjacentHTML("afterbegin", liTag);
    })
}

function removeTag(element, tag) {
    let index = tags.indexOf(tag);
    tags.splice(index, 1);
    console.log(tags);
    element.remove();
}

function addTag(e) {
    if(e.key == ",") {
        let tag = e.target.value.replace(",","")
        if (tag.length > 0 && !tags.includes(tag)) {
            tags.push(tag);
            removeTags();
            createTags();
        }
        e.target.value = "";
    }
}

function backspaceToRemoveTag(e) {
    if (e.key == "Backspace") {
        if (e.target.value.length == 0) {
            tags.pop();
            removeTags();
            createTags();
        }
    }
}



input.addEventListener("keyup", addTag);
input.addEventListener("keydown", backspaceToRemoveTag);

function submitForm() {
    let form = document.querySelector("form");
    let currentInput = input.value;
    if (currentInput.length > 0  && !tags.includes(currentInput)) {
        tags.push(currentInput);
    }
    let tagsString = tags.join(",")
    let tagsInputField = document.createElement("input");
    tagsInputField.setAttribute("name", "user_properties");
    tagsInputField.setAttribute("value", tagsString);
    tagsInputField.hidden = true;
    form.append(tagsInputField);
    form.submit();
}

function presetForm(name, userProperties) {
    document.getElementsByName("name")[0].value = name;
    if (userProperties != "") {
        userPropertiesArr = userProperties.split(",");
        tags.push(...userPropertiesArr);
        createTags();
    }
}