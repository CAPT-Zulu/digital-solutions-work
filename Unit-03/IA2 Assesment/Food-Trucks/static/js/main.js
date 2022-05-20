///// Testing NavBar /////
// const navbarToggle = Header.querySelector("#navbar-toggle");
// const navbarMenu = document.querySelector("#navbar-menu");
// const navbarLinksContainer = navbarMenu.querySelector(".navbar-links");
// let isNavbarExpanded = navbarToggle.getAttribute("aria-expanded") === "true";
//
// const toggleNavbarVisibility = () => {
//   isNavbarExpanded = !isNavbarExpanded;
//   navbarToggle.setAttribute("aria-expanded", isNavbarExpanded);
// };
//
// navbarToggle.addEventListener("click", toggleNavbarVisibility);
//
// navbarLinksContainer.addEventListener("click", (e) => e.stopPropagation());
// navbarMenu.addEventListener("click", toggleNavbarVisibility);

///// Testing Maps /////
// var map = L.map('Map-Main-Page').setView([-27.474, 153.038], 10.21);
// L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//     // maxZoom: 17,
//     // minZoom: 9,
//     id: 'mapbox/streets-v11',
//     tileSize: 512,
//     zoomOffset: -1,
//     accessToken: 'pk.eyJ1IjoiMjU1ODgiLCJhIjoiY2wyZ3lya3RmMDhxODNjcHJkMjRpc2Q2diJ9.jrOtIuFfbNHHHpTIN3wbfA'
// }).addTo(map);
// var marker = L.marker([-27.474, 153.038]).addTo(map);
// fetch("/static/jsons/geodata.json")
//   .then(response => response.json())
//   .then(json => L.geoJson(json).addTo(map));
// L.geoJson(data).addTo(map);
// async function main() {
//     var map = L.map('Map-Main-Page').setView([-27.474, 153.038], 10.21);
//     L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//         attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//         // maxZoom: 17,
//         // minZoom: 9,
//         id: 'mapbox/streets-v11',
//         tileSize: 512,
//         zoomOffset: -1,
//         accessToken: 'pk.eyJ1IjoiMjU1ODgiLCJhIjoiY2wyZ3lya3RmMDhxODNjcHJkMjRpc2Q2diJ9.jrOtIuFfbNHHHpTIN3wbfA'
//     }).addTo(map);
//     var marker = L.marker([-27.474, 153.038]).addTo(map);
//     // fetch("/static/jsons/geodata.json")
//     //     .then(response => response.json())
//     //     .then(json => L.geoJson(json).addTo(map));
//     // L.geoJson(data).addTo(map);
// }
//
// document.onload = main()

///// Testing Multi input /////
// class MultiInput extends HTMLElement {
//   constructor() {
//     super();
//     // This is a hack :^(.
//     // ::slotted(input)::-webkit-calendar-picker-indicator doesn't work in any browser.
//     // ::slotted() with ::after doesn't work in Safari.
//     this.innerHTML +=
//     `<style>
//     multi-input input::-webkit-calendar-picker-indicator {
//       display: none;
//     }
//     /* NB use of pointer-events to only allow events from the × icon */
//     multi-input div.item::after {
//       color: black;
//       content: '×';
//       cursor: pointer;
//       font-size: 18px;
//       pointer-events: auto;
//       position: absolute;
//       right: 5px;
//       top: -1px;
//     }
//
//     </style>`;
//     this._shadowRoot = this.attachShadow({mode: 'open'});
//     this._shadowRoot.innerHTML =
//     `<style>
//     :host {
//       border: var(--multi-input-border, 1px solid #ddd);
//       display: block;
//       overflow: hidden;
//       padding: 5px;
//     }
//     /* NB use of pointer-events to only allow events from the × icon */
//     ::slotted(div.item) {
//       background-color: var(--multi-input-item-bg-color, #dedede);
//       border: var(--multi-input-item-border, 1px solid #ccc);
//       border-radius: 2px;
//       color: #222;
//       display: inline-block;
//       font-size: var(--multi-input-item-font-size, 14px);
//       margin: 5px;
//       padding: 2px 25px 2px 5px;
//       pointer-events: none;
//       position: relative;
//       top: -1px;
//     }
//     /* NB pointer-events: none above */
//     ::slotted(div.item:hover) {
//       background-color: #eee;
//       color: black;
//     }
//     ::slotted(input) {
//       border: none;
//       font-size: var(--multi-input-input-font-size, 14px);
//       outline: none;
//       padding: 10px 10px 10px 5px;
//     }
//     </style>
//     <slot></slot>`;
//
//     this._datalist = this.querySelector('datalist');
//     this._allowedValues = [];
//     for (const option of this._datalist.options) {
//       this._allowedValues.push(option.value);
//     }
//
//     this._input = this.querySelector('input');
//     this._input.onblur = this._handleBlur.bind(this);
//     this._input.oninput = this._handleInput.bind(this);
//     this._input.onkeydown = (event) => {
//       this._handleKeydown(event);
//     };
//
//     this._allowDuplicates = this.hasAttribute('allow-duplicates');
//   }
//
//   // Called by _handleKeydown() when the value of the input is an allowed value.
//   _addItem(value) {
//     this._input.value = '';
//     const item = document.createElement('div');
//     item.classList.add('item');
//     item.textContent = value;
//     this.insertBefore(item, this._input);
//     item.onclick = () => {
//       this._deleteItem(item);
//     };
//
//     // Remove value from datalist options and from _allowedValues array.
//     // Value is added back if an item is deleted (see _deleteItem()).
//     if (!this._allowDuplicates) {
//       for (const option of this._datalist.options) {
//         if (option.value === value) {
//           option.remove();
//         };
//       }
//       this._allowedValues =
//       this._allowedValues.filter((item) => item !== value);
//     }
//   }
//
//   // Called when the × icon is tapped/clicked or
//   // by _handleKeydown() when Backspace is entered.
//   _deleteItem(item) {
//     const value = item.textContent;
//     item.remove();
//     // If duplicates aren't allowed, value is removed (in _addItem())
//     // as a datalist option and from the _allowedValues array.
//     // So — need to add it back here.
//     if (!this._allowDuplicates) {
//       const option = document.createElement('option');
//       option.value = value;
//       // Insert as first option seems reasonable...
//       this._datalist.insertBefore(option, this._datalist.firstChild);
//       this._allowedValues.push(value);
//     }
//   }
//
//   // Avoid stray text remaining in the input element that's not in a div.item.
//   _handleBlur() {
//     this._input.value = '';
//   }
//
//   // Called when input text changes,
//   // either by entering text or selecting a datalist option.
//   _handleInput() {
//     // Add a div.item, but only if the current value
//     // of the input is an allowed value
//     const value = this._input.value;
//     if (this._allowedValues.includes(value)) {
//       this._addItem(value);
//     }
//   }
//
//   // Called when text is entered or keys pressed in the input element.
//   _handleKeydown(event) {
//     const itemToDelete = event.target.previousElementSibling;
//     const value = this._input.value;
//     // On Backspace, delete the div.item to the left of the input
//     if (value ==='' && event.key === 'Backspace' && itemToDelete) {
//       this._deleteItem(itemToDelete);
//     // Add a div.item, but only if the current value
//     // of the input is an allowed value
//     } else if (this._allowedValues.includes(value)) {
//       this._addItem(value);
//     }
//   }
//
//   // Public method for getting item values as an array.
//   getValues() {
//     const values = [];
//     const items = this.querySelectorAll('.item');
//     for (const item of items) {
//       values.push(item.textContent);
//     }
//     return values;
//   }
// }
//
// window.customElements.define('multi-input', MultiInput);

///// Testing Search System /////
const Search = (input, elements, parent) => {
    let result = 0;

    // For every element to search through check if the element is related to the search query and hide it if it doesn't
    for (const element of elements) {
        if (element.innerHTML.toLowerCase().includes(input.value.toLowerCase())) {
            element.parentElement.parentElement.style.display = 'flex';
            result++;

        } else {
            element.parentElement.parentElement.style.display = 'none';
        }
    }

    // If there are no results show a message (edit this to remove the option to not sure the error msg)
    const errormsg = document.querySelector('.search-noresults');

    if (!result) {
        const msgelement = document.createElement('h1');
        msgelement.innerHTML = 'No results found';
        msgelement.classList.add('search-noresults');

        if (!errormsg) {
            parent.appendChild(msgelement);
        }
    } else {
        if (errormsg) {
            errormsg.remove();
        }
    }
};