'use strict';

window.onresize = () => {
    fixHeight();
}

function fixHeight() {
    const canvas = document.getElementById("background-canvas");
    if (!canvas) {
        return;
    }
    const postDetail = document.querySelector(".post-detail");
    const ctx = canvas.getContext("2d");

    canvas.width = postDetail.offsetWidth;
    canvas.height = postDetail.offsetHeight;
    // ctx.fillStyle  = "rgba(	127, 0, 255, 0.3)";
    // ctx.fillRect(0, 0, canvas.width, canvas.height)
};

function typingEffect(container) {

    const typingContainer = container
    
        if (typingContainer) {
            const text = typingContainer.innerHTML;
                        
            typingContainer.innerHTML = ""; // Clear content to start typing effect
            // remove class content-hidden
            typingContainer.classList.remove("content-hidden");

            // Function to simulate typing effect
            let index = 0;
            let elementToAppend = typingContainer;
    
            function typeEffect() {
            if (index < text.length) {
                // detect any tags and create a new element to append the text
                if (text[index] === "<") {
                    let tag = "";
                    while (text[index] !== ">") {
                        tag += text[index];
                        index++;
                    }
    
                    tag += ">"; // Add closing tag
    
                    // check if tag is a closing, opening tag or self-closing tag

                    // check if it's a closing tag
                    if (tag.startsWith("</")) {
                        // reset to parent element
                        elementToAppend = elementToAppend.parentElement;
                    }
                    else {
                        let tagName = tag.slice(1, tag.length - 1);
                        // console.log(tag);
                        // console.log(tagName);

                        // create a new element based on the tag name
                        tagName = tagName.split(" ")[0]; // get only the tag name

                        let newElement = document.createElement(tagName);
                        elementToAppend.appendChild(newElement);
                        elementToAppend = newElement;
                        
                        // parse the tag attributes
                        let attributes = tag.match(/\S+=".*?"/g);
                        if (attributes) {
                            attributes.forEach(attribute => {
                                let [attributeName, attributeValue] = attribute.split("=");
                                attributeValue = attributeValue.slice(1, attributeValue.length - 1);
                                elementToAppend.setAttribute(attributeName, attributeValue);
                            });
                        }

                        // check if it's a self-closing tag
                        if (tag.endsWith("/>") || tagName === "img") {
                            // reset to parent element
                            elementToAppend = elementToAppend.parentElement;
                        }

                    }

                    index++;
                }
    
                // Append text to the new element
                elementToAppend.innerHTML += text[index];
    
                index++;

                fixHeight();

                setTimeout(typeEffect, 0.1); // Adjust typing speed here
            } else {
                htmx.process(document.getElementById("page-text"));
            }
            }
            typeEffect(); // Start typing effect
        }
    }