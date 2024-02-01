const BASE_URL = "http://localhost:5000/api";
const $cupcakeList = $('#cupcake-list');

async function getCupcakes(){
    const response = await axios.get(`${BASE_URL}/cupcakes`)
    return response.data.cupcakes
}

function generateCupcakes(cupcakes){
    $cupcakeList.empty()
    for(let cupcake of cupcakes){
        const $cupcakeLi = $('<li>')

        const $cupcakeImage = $('<img>');
        $cupcakeImage.attr('src', cupcake.image);
        $cupcakeImage.attr('alt', `Cupcake Image - ${cupcake.flavor}`);
        $cupcakeLi.append($cupcakeImage)

        
        $cupcakeLi.append(`Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}`)
        $cupcakeList.append($cupcakeLi)
    }
}

$(document).ready(async function(){
    const cupcakes = await getCupcakes();
    generateCupcakes(cupcakes)});
    $('#new-cupcake-form').submit(handleFormSubmit);


    
async function createCupcake(data){
    const response = await axios.post(`${BASE_URL}/cupcakes`, data);
}
async function handleFormSubmit(evt){
    evt.preventDefault();
    const data = {
        flavor: $('input[name="flavor"]').val(),
        size: $('input[name="size"]').val(),
        rating: $('input[name="rating"]').val(),
        image: $('input[name="image"]').val()
    }
    createCupcake(data)
    const cupcakes = await getCupcakes();
    generateCupcakes(cupcakes)};
