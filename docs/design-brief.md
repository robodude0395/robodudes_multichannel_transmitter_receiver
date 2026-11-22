Custom multichannel transmitter

Inputs:
>Two 4 axis joysticks. Pitch and roll as usual plus yaw by twisting the stick and a button for another input
>Two potentiometers
>Two toggle switches
>Two trigger switches
>Two dpads on each side of the screen used for menu navigation which total to 8 buttons
>A program port which will be on the outside case to allow for each re-programming of radio. Whether it's UART or USB is to be decided

Outputs:
>The nrf-24l01 transmitter
>A 1.8 inch st7735 screen
>A PS2 training port to allow for telemetry just like the Flysky radio
>A buzzer for tones

WHAT NEEDS WORKING OUT:
>Should the programming port be USB or uart? this is dependant on the choice of inner microcontroller which at the moment is an stm32 but might need an auxiliary board to accomodate the extra inputs or there might be simply be a better single board option that can handle this entire workload.
>Circuit for measuring battery voltage.
>Work out a user experience document for how the user will navigate the pages in the transmitter.
>Receiver voltage telemetry circuit.

Radio protocol:
So far using the regular nrf protocol has worked. I've had reliability issues trying to implement frequency hopping in the past and I've also heard of open firmware protocols such as ELRS and Crossfire. Im open to consider options. I need good reliability and range. I'll be using an nrf24l01 and pa module for the transmitter.

Features (In no particular order):
>Freedom to assign radio inputs to channel outputs. Outputs will be standard pwm signals every transmitter uses. For example by navigating through the screen's interface I should be able to set the input for a toggle button to any channel I want, be it channel 1, 2 3, 4. This will be relevant with the profile setting feature later on where profiles are stored as json configs in the sd card from the screen.
>Reversable inputs.
>Programmable dual rates for each channel. I tried out flysky's endpoint and exp setting where you can set any input's curve. I want to replicate that for all the inputs. Each curve should be set with those two parameters.
>I want the interface to be pretty. By that I mean use of a consisent colour palette. I want a sharp black background for elements alongside white contrasting borders and black text within appropiate elements. I also want to get artsy with it so during development I want ot add in placeholder graphics, gifs and animations to visualize how the interface experience and navigation will be.
>Ability to trim inputs through a menu navigation option just like with the ability to assign dual rates.
>Mixable inputs. Im still somewhat unclear on how this one can work. What I am thinking is an option to sum, multiply two inputs toghether into one channel. Im still flaky on this implementation so working on this feature should not break the others. For example I am thinking of having a toggle switch add a certain amount to an input or multiply it by a certain amount. Similar to throttle hold in flysky transmitters
>A 'weird port' this is a port where I could connect usb peripherals and gamepads to add even more fun to the tranmitter. Now instead of controlling an rc plane with the transmitter, I can hook up an xbox controller, get the transmitter to see all the extra inputs like a usb HID peripheral and then assign those peripherals to channels.
>A standard default profile that cannot be changed. Any saved changes to the profile must be saved as a separate profile. as mentioned before, profiles may be saved in human readable formats in the sd card such as json.
>A battery % indicator on the top left of the screen. Circuitry on how to do this is yet to be worked out
>Profile settings that save all the endpoints and features described so far. Basically any changes done to input mapping, dual rates, endpoints, etc, must be saved into a profile witin the sd card which gets loaded on startup. When a profile is loaded on startup, it'll revert to it's default if it's not found. Otherwise if the profile is not saved, then the radio forgets. Even simpler I could just take a page out of flyysky and just have a bunch of profiles (about 50) where one is default and is used to reset everything as a reset defaults option.
>A fun aesthetic for menu items. In these menu items I keep visualizing a small catgirl mascot or similar like the flipper zero who toys and plays around. When something loads you see it playing with it's transmitter, in the background it'll be leaning or dancing a bit... My idea is to get some placeholders that do not require images or use generated placeholders and come back to inser them. once the transmitter is actually done. I really want some gif or animations going around.
>The buzzer will play tunes when turning on and play beeps when scrolling through the options just like the flysky radio. GUI experience will be it's own workflow
>Joystick calibration option where you calibrate input joysticks. this includes the onboard joysticks and the input ones from an external gamepad connected via usb.
>there are three workflows I've identified so far that can run in parallel. On workflow is Gui another is code and another is testing.
>Most testing will be manual, does the radio work, do screen elements show? But for the GUI I also want a software tool that'll allow me to emulate the screen and User experience. This is essentially my virtual transmitter that I can play around in, save profiles, navigate through the GUI ad test out features before putting them in the transmitter.
>Ability to read voltage of the model back from the receiver just like a malenki. this relates to the receiver circuit/receiver which I intentially want to be dead simple, just output values received from radio and report back the system voltage. cicuitry for receiving system voltage is also to be worked out.
>An indicator on the top left to show two statuses. The status of the transmitter radio module and the status of the receiver radio ie: Has the transmitter detected a radio at all? Indicate red if not ok. Indicate green if ok.


CODE PRACTICES:
DRY (Dont Repeat Yourself)
KISS (Keep It Simple)
Solid Principles
Dont let a feature indirectly break the other.
De-coupling ensure features are decoupled from each other. For example if the mixing feature does not work or has a bug, if it's diabled, then it should not interrupt transmission from an input to a channel
Ensure to tackle core functionality first before tackling the features that are dependant on the core first. I first want a radio that outputs to some channels. It does not matter if they are mappable or mixable or anything. Just the bare basics to confirm the radio IO works. The core will be the input buttons, joysticks, etc and it's output is the radio, the screen (just graphics text) and the buzzer.
