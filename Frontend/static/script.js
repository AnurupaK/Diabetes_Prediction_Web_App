let stopTyping = false;
let ready_tochat_global = 0;
document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.submit_button').addEventListener('click', async function () {
        const stop = document.querySelector('.stop_button')
        const screen = document.querySelector('.chat_area');
        screen.innerHTML = '';
        const previousMessage = screen.querySelector('.message_area');
        if (previousMessage) {
            screen.removeChild(previousMessage);
        }

        const glucose = parseFloat(document.getElementById('glucose').value);
        const bp = parseFloat(document.getElementById('bp').value);
        const insulin = parseFloat(document.getElementById('insulin').value);
        const bmi = parseFloat(document.getElementById('bmi').value);
        const age = parseFloat(document.getElementById('age').value);
        if (typeof glucose === 'number' && typeof bp === 'number' && typeof insulin === 'number' && typeof bmi === 'number' && typeof age === 'number') {

            const data_input = {
                glucose: glucose,
                bp: bp,
                insulin: insulin,
                bmi: bmi,
                age: age
            };

            const { message, value_msg } = await sendData_to_backend(data_input);
            console.log(message, value_msg);

            let msg = document.createElement('div');
            msg.className = 'message_area';
            screen.insertAdjacentElement('afterbegin', msg);
            msg.innerHTML = "<span class='emoji' style='font-size: 24px;'>👨🏻‍⚕️</span>";
            stopTyping = false; // Reset the stop flag
            await typeEffect(msg, message);

            if (value_msg == 1) {
                const outcome_screen = document.getElementById('result');

                let { outcome, check, ifDB } = await checkDB(data_input);
                console.log(outcome, check);
                setTimeout(() => {
                    if (ifDB) {
                        outcome_screen.style.backgroundImage = 'none';
                        outcome_screen.style.backgroundColor = 'pink';
                    }
                    else {
                        outcome_screen.style.backgroundImage = 'none';
                        outcome_screen.style.backgroundColor = 'green'
                    }
                    outcome_screen.value = outcome;
                    outcome_screen.style.fontSize = '1.5rem';
                    outcome_screen.style.fontWeight = 'bold'


                    if (check == 1) {
                        setTimeout(async () => {
                            var div2 = document.querySelector(".message_area");
                            div2.remove();
                            const { doc_response, ready_to_chat } = await doctorResponse(outcome, glucose, bp, insulin, bmi, age);
                            console.log(`Ready to chat ${ready_to_chat}`);
                            ready_tochat_global = ready_to_chat
                            console.log("To check if ready to chat global turned 1:", ready_tochat_global)

                            if(ready_tochat_global==1){
                                document.querySelector(".gbutton").addEventListener('click', async function () {
                                    console.log("Generate report button clicked");
                                        const { gluR, bpR, insulinR, bmiR, ageR, outcomeR } = await getInputs();
                                        console.log("Inputs fetched", gluR, bpR, insulinR, bmiR, ageR, outcomeR, doc_response );
                            
                                        localStorage.setItem('glucose', gluR);
                                        localStorage.setItem('bp', bpR);
                                        localStorage.setItem('insulin', insulinR);
                                        localStorage.setItem('bmi', bmiR);
                                        localStorage.setItem('age', ageR);
                                        localStorage.setItem('outcomeR', outcomeR);
                                        localStorage.setItem('doc',doc_response)
                            
                                        setTimeout(()=>{
                                            window.location.href = "report.html";
                                        },2000)
                                })
                            }else{
                                console.error("Can't generate report")
                            }

                            let doc = document.createElement('div');
                            doc.className = 'bot chat_box';
                            screen.appendChild(doc);

                            stop.addEventListener('click', function () {
                                stopTyping = true;
                            });

                            stopTyping = false; // Reset the stop flag
                            await typeEffect(doc, doc_response);

                            if (ready_to_chat == 1) {
                                console.log("I am inside");
                                document.querySelector('.cbutton').addEventListener('click', async function () {
                                    const chatDisplay = document.querySelector('.chat_area');
                                    const userTxt = document.getElementById('userInput');

                                    if (userTxt.value.trim() !== "") {
                                        let userMessage = document.createElement('div');
                                        userMessage.className = 'user chat_box';
                                        userMessage.innerHTML = "<span class='emoji' style='font-size: 30px;'>👩🏻‍🦰</span> " + userTxt.value;
                                        chatDisplay.appendChild(userMessage);

                                        let botMessage = document.createElement('div');
                                        botMessage.className = 'bot chat_box';

                                        let botResponse = await getBotResponse(userTxt.value);
                                        botMessage.innerHTML = "<span class='emoji' style='font-size: 24px;'>👨🏻‍⚕️</span> ";
                                        chatDisplay.appendChild(botMessage);
                                        userTxt.value = "";

                                        stop.addEventListener('click', function () {
                                            stopTyping = true;
                                        });

                                        stopTyping = false; // Reset the stop flag
                                        await typeEffect(botMessage, botResponse);

                                        chatDisplay.scrollTop = chatDisplay.scrollHeight;
                                    }
                                });
                            }
                        }, 3000);
                    }
                }, 2000);
            }
        } else {
            console.error("Inputs are not numbers");
        }
    });
});

async function sendData_to_backend(data) {
    try {
        let dataSent = await fetch('/api/Inputs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        let response = await dataSent.json();
        return {
            message: response.message,
            value_msg: response.value_msg
        };
    } catch (error) {
        console.log('Error sending data to backend', error);
    }
}

async function typeEffect(element, text) {
    const typingSpeed = 50;
    let i = 0;
    while (i < text.length && !stopTyping) {
        element.innerHTML += text.charAt(i);
        i++;
        await new Promise((resolve) => setTimeout(resolve, typingSpeed));
    }
}

async function checkDB(inputs) {
    try {
        let response = await fetch('/api/checkDiabetes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inputs)
        });
        let data = await response.json();
        return {
            outcome: data.outcome,
            check: data.check,
            ifDB: data.ifDB
        };
    } catch (error) {
        console.log("Model couldn't predict", error);
    }
}

async function doctorResponse(outcome, glucose, bp, insulin, bmi, age) {
    try {
        let response = await fetch('/api/get_doc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ outcome, glucose, bp, insulin, bmi, age })
        });
        let data = await response.json();
        return {
            doc_response: data.doc_response,
            ready_to_chat: data.ready_to_chat
        };
    } catch (error) {
        console.log("Doctor didn't give response", error);
    }
}

async function getBotResponse(user_text) {
    try {
        let response = await fetch('/api/start_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_response: user_text })
        });
        let data = await response.json();
        return data.bot_response;
    } catch (error) {
        console.error("Not able to chat for some issue", error);
        return "Server down";
    }
}

async function getInputs() {
    try {
        let response = await fetch('/api/getData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        let data = await response.json()
        return {
            gluR: data.glucose,
            bpR: data.bp,
            insulinR: data.insulin,
            bmiR: data.bmi,
            ageR: data.age,
            outcomeR: data.outcome,
            doc: data.doc_response

        }

    } catch (error) {
        console.log("Error Fetching Inputs", error)
    }
}



