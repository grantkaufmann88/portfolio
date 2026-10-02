# Website copy - current edition

Readable export of `content/projects.json`. Edit the JSON and rebuild to change the site.

## Vera Rubin Observatory transducer positioning system

An ongoing two-axis robotic actuator, custom strain-wave drive, and control system for precisely aiming an ultrasonic time-of-flight temperature-measurement array.

**Role:** Mechanical, electronics, and control-system design, Rowland Institute

**Status:** Currently Working On

### Why this measurement matters

Vera C. Rubin Observatory sits on Cerro Pachon in Chile and uses the 8.4-meter Simonyi Survey Telescope and 3.2-gigapixel LSST Camera to repeatedly image the southern sky. The observatory began its ten-year Legacy Survey of Space and Time in 2026. Harvard professor Christopher Stubbs, Rubin's inaugural project scientist, leads a group working with the observatory.

The instrument I am helping develop is aimed at a different but related problem: characterizing the air above the telescope optics. Temperature changes alter air density and therefore the optical path through the atmosphere. The proposed measurement sends directional ultrasonic pulses across the telescope and uses time of flight to infer the temperature along the path. My work is on the ultrasonic array, its positioning actuator, and the control electronics - not the telescope pointing system itself.

### Turning a measurement requirement into a robotics problem

The basic measurement only requires the transducer array to be aimed over a small angular range, and a geared servo linkage could have met that need. I chose to use the project as an opportunity to build a more general two-degree-of-freedom actuator that can be positioned remotely through a full rotation.

The target pointing accuracy is 0.1 degree. That is a design requirement agreed on with the researchers, not a measured accuracy result yet. Multiple retroreflectors around the telescope are a possible extension for sampling several paths through the air, but that is a nice-to-have rather than a requirement.

### Designing a printable 50:1 strain-wave drive

Each axis uses a NEMA 17 stepper motor and a custom 50:1 strain-wave gearbox. With a 200-step-per-revolution motor, one full motor step corresponds to a theoretical output increment of about 0.036 degree before accounting for backlash, compliance, print error, and microstepping behavior.

I chose a printed strain-wave drive because commercial metal units are expensive and difficult to manufacture from scratch, and because the geometry was a useful design challenge. The flex spline has 98 teeth against a 100-tooth fixed spline. Instead of coupling the output directly through a long cup-shaped flex spline, I separated the output and used a second 98-tooth interface. The goal is to keep deformation localized and reduce the layer-line stresses that concern me in a printed cup.

### Integrating the bearings instead of packaging catalog parts

The gearbox uses printed bearing races with loose steel bearing balls rather than conventional packaged bearings in several locations. Ball arrays around the elliptical wave generator let the flex spline move smoothly while keeping the assembly compact.

I also used thrust-bearing arrangements to react axial loading and the overturning moment from the transducer assembly. One external bearing helps hold the assembly together in tension while internal bearings resist compression. I may move toward tapered or deep-groove bearings in a later version as I learn more from the load path and prototype behavior.

### FDM first, then resin - and a new DFM problem

I deliberately made the first gearbox in FDM because it was fast and inexpensive. It proved the basic geometry, but friction and tolerance variation were high, especially around the small tooth profiles. I then adjusted the clearances and moved the design to tough resin.

The resin version improved feature definition but introduced a different problem: parts warped because the geometry had originally been designed around FDM. I am now redesigning those parts for resin manufacturing rather than treating the new process as a drop-in replacement. The video above shows the resin-printed gearbox prototype.

### Two boards, two axes, and one cable carrying power and commands

The actuator uses two NEMA 17 motors and custom electronics. The actuator board schematic uses an ATtiny1604 microcontroller and two DRV8434A stepper drivers. A separate hand-control board uses another ATtiny1604, a CAP1298 capacitive-touch controller, a joystick, an LCD connection, USB through a CH340C, and a UCC27211 half-bridge gate driver with IRLR7843 MOSFETs to switch the 12 V line.

A packaging constraint from the lab was to use a long DC twisted pair for both power and commands. My approach is to encode a one-wire UART signal by switching the 12 V supply. At the actuator, a diode and reservoir capacitance maintain DC power while a high-pass path and comparator recover the data transitions. I selected a relatively high signaling rate so the energy-storage capacitor can remain practical. The exact data rate is still being finalized in firmware; the narration included conflicting 100 kHz / 100 bit-per-second wording, so I am not publishing an unverified baud-rate number.

### Open-loop positioning, with a laser for setup and validation

I chose not to add absolute encoders at this stage. The load is light, the stepper reduction gives substantial holding torque, and the array can be manually referenced at setup. From that known position, the controller can track relative motion as long as the motors do not miss steps. A laser mounted with the array provides a practical aiming reference.

To validate the 0.1-degree requirement, I plan to rigidly mount the actuator and use a long-baseline laser test. I will command individual steps, measure the laser-spot displacement on a distant target, convert that displacement to angle, and repeat the test in both directions. Direction reversals will let me quantify backlash and hysteresis rather than treating theoretical step size as achieved accuracy.

### Where the project is now

The mechanical concept has progressed through FDM and resin gearbox prototypes, and the complete two-axis assembly, control board, and actuator board have been designed. As of this update, I am waiting for the two PCBs to be fabricated, revising the resin parts for manufacturability, and beginning firmware for the control system.

The hand controller is designed around a joystick, capacitive-touch inputs, and an LCD that will show commanded angular position and system status. The finished accuracy, reliability, and temperature-measurement performance remain to be demonstrated; those are the next tests, not claims about the current prototype.

## Micro swarming drone

An ongoing low-cost drone design with custom electronics and a camera, aimed at autonomous landing, charging, and cooperative tasks.

**Role:** Independent project

**Status:** Currently Working On

### Making each drone inexpensive enough to work in a group

I am developing a small drone around a simple goal: make an individual vehicle inexpensive enough that several can work together. My current high-volume cost estimate is about $22 per drone, and I am still trying to reduce it. That is an estimate for the design, not the purchase price of a completed product.

The longer-term idea is for drones to swap tasks while others land or recharge, instead of depending on a single vehicle to stay airborne indefinitely.

### Integrating the electronics and camera

The design combines STM32 and ESP32 processing with an OV2640 camera. The custom flight-control electronics and drivers need to fit into a compact central board, surrounded by a lightweight frame and propeller guards.

The earlier design targeted a mass of approximately 52 g and a board under 5 cm across. The CAD and board images show the packaging work; they are not evidence of a finished autonomous fleet.

### What remains to be demonstrated

This is still an early-stage project. Automatic takeoff, landing, charging, coordinated tasks, and a flight time of about 20 minutes are goals. They have not yet been demonstrated as an integrated system.

The current work is on the aircraft and its custom electronics. Reliable autonomous operation is the next layer, not a capability I am claiming for the prototype today.

## Budget e-bike conversion kit

A custom motor controller, removable battery enclosure, and experimental printed motor for an affordable bicycle conversion.

**Role:** Independent project

**Status:** Bench-tested controller; printed motor limited by heat

### A conversion kit, not a new bicycle

I wanted to make electric transportation more affordable by adding power to a bicycle someone already owns. I set a materials-cost target below $150, with a stretch goal below $100. Easy installation, a removable battery, straightforward maintenance, and low-cost manufacturing were central design requirements.

An initial attempt in 2020 stalled when I did not yet have the tools or electronics background to finish it. I returned to the project after building my own circuit-board mill and studying circuits and electromagnetism. The later prototype was divided into three systems: rider controls, a battery-and-electronics enclosure, and a motor.

### Designing the sensorless motor controller

The electronic speed controller was the hardest part of the kit. I designed three MOSFET half-bridges around an ATmega328P microcontroller, with gate-driver chips controlling the power transistors. Rather than adding a rotor-position sensor, I used the voltage generated in the phase that was not being driven to work out when to switch phases.

At each step, two motor phases were driven while the third was left floating. Monitoring that floating phase's back-EMF zero crossing gave the controller information about the rotor position. Avoiding a separate sensor reduced the number of parts and connections I would have to package and protect on a bicycle.

The board also brought together a thumb throttle and an HM-10 Bluetooth module. Bench tests demonstrated control of a small brushless drone motor, detection of the generated voltage signal, throttle response, and two-way communication with an iPhone.

### The enclosure and bike interface

I designed the battery housing, mounting system, and electrical connections as one assembly. A PETG enclosure held the batteries and controller, with flexible TPU seals and spring-loaded clips for removal from the bicycle. The prototype used two four-cell battery packs in series.

The enclosure work was about more than fitting the parts into a box: the battery needed to be removable, the throttle and motor needed accessible connections, and heat from the electronics needed somewhere to go. Weather sealing was a design goal, not a tested waterproof rating.

### When making everything myself stopped helping

At first I milled and soldered the boards at home. I also tried building the transistor-driving circuitry from individual components. Troubleshooting fast switching signals with only a multimeter was frustrating, and the closely spaced copper on boards without solder mask made assembly difficult.

After more than 50 board attempts, I changed the process. I bought a used digital oscilloscope, switched to integrated gate-driver chips, and outsourced the board fabrication. Those changes let me spend more time developing the controller and less time fighting the limitations of my tools.

### Testing a printed motor

I also designed an experimental hub motor and wound its coils by hand. After an early plastic stator produced very little voltage when spun, I tried an iron-filled PLA core and a Halbach arrangement of permanent magnets, intended to concentrate the magnetic field toward the windings.

The motor turned, but heat softened and deformed the printed core under load. That was a material limit, not just a controller problem. Printing the geometry was useful for prototyping, but the core also had to survive the heat of an operating motor. The controller tests and printed-motor experiments were steps toward the kit, not a completed production-ready bicycle conversion.

### The next design decision

My proposed next step was a laminated metal stator paired with the controller and removable enclosure I had already developed. The 2024 component estimate was $82.74 excluding the motor. That was a prototype estimate, not an achieved retail price or the cost of a complete commercial product.

## Desktop CNC / PCB mill

A home-built three-axis mill that produced circuit boards for my e-bike, home controller, and other electronics.

**Role:** Independent project

**Status:** Built and used

### Building the tool I needed

I wanted to make custom circuit boards at home without waiting for every revision to be manufactured elsewhere. I designed a small three-axis mill that removes copper around the traces on a circuit board. The machine became both a project in its own right and a tool for nearly everything I built afterward.

### A low-cost frame and open-source control

I modeled the machine in Onshape and used 80/20 aluminum extrusion joined by custom printed brackets. Steel linear guides, threaded rods, and stepper motors provided the three axes of motion, with a 24 V DC spindle doing the cutting. The earlier design had approximately 275 by 175 by 35 mm of planned travel.

An Arduino running GRBL controlled the axes. My workflow started with PCB Gerber files in FlatCAM, then passed the machining commands to the controller over USB. The machine connected the circuit layout on my computer to a board I could mill and assemble at home.

### The first version was not rigid enough

My first approach used inexpensive zinc-plated rods and resin-printed bearings instead of precision linear hardware. The combination introduced too much friction, instability, and positioning error for reliable circuit-board work. I abandoned that arrangement and revised the machine through several versions.

Unlike a 3D printer, this machine had to push a tool through material. That distinction turned stiffness, bearing friction, and assembly alignment into practical design problems rather than just dimensions in a CAD model.

### The version after the build videos

The machine in my YouTube build videos was not the final version. I continued revising it afterward until it could reliably produce the double-sided copper-clad boards I needed. I used those boards in the e-bike controller, smart home controller, go-kart, and other projects.

The plastic structure remained the main limitation. It worked well for PCB isolation milling and could make some simple aluminum parts, but it was not a sufficiently rigid platform for the broader aluminum and steel machining I had hoped to do. Producing useful circuit boards and producing a general-purpose metal mill turned out to be very different goals.

### Knowing when to use another process

The mill could form traces, but it could not give me solder mask or the full set of features of a professionally manufactured board. Dense circuits became difficult to assemble without shorts. When that became the main obstacle to the e-bike project, I kept designing the electronics myself but sent the board files out for fabrication.

Building the mill taught me to treat manufacturing capability as part of a design decision: a tool can be valuable without being the right tool for every later version.

## Mini Cybertruck go-kart

A welded steel go-kart with electronic steering, remote control, and a custom starter-generator transmission.

**Role:** Independent project

**Status:** Built; integration documented in 2024

### A project that grew with me

The first version was a wooden go-kart I worked on over several summers. Repeated damage eventually pushed me toward a welded steel frame. I bought scrap steel on Facebook Marketplace, laid out the parts from my CAD model, and continued building under a tent in my backyard through the winter. A repurposed gaming chair became the seat.

The later version combined a 212 cc Predator engine, a continuously variable transmission, and a body inspired by the Cybertruck. Much of the challenge came from choosing electronic steering and controls rather than a conventional mechanical connection between the driver and the wheels.

### Building an electronic steering system

I converted a 12 V motor into a steering actuator by adding output-position feedback through a potentiometer. A printed steering horn moved the steering bar, while the controller compared the measured steering position with the driver's request.

The steering wheel had its own spring return because it was not mechanically connected to the front wheels. Triggers on its handles controlled throttle and braking through separate servos. I designed the control board and manufactured it on my homemade CNC. The same electronic interface also let me operate the kart remotely, which made it easier to test parts of the system without a driver in the seat.

### One motor for starting and charging

The most interesting mechanism was the starter-generator. An electric motor needed high mechanical advantage to turn the engine through compression during starting, but a different ratio once the running engine drove it as a generator.

I designed a belt transmission with printed components and one-way bearings that changed the ratio from 9:1 during starting to 1:1 when driven by the engine. The difficult part was not only getting the mechanism to switch roles, but making the printed parts withstand the starting torque.

### Integrating the rest of the vehicle

The wiring brought together steering, throttle and brake actuators, engine cutoff, power distribution, and lighting. I also built servo-driven dashboard gauges, added Bluetooth audio, and experimented with a printed supercharger. The supercharger did not add much power; it was more useful as an impeller and fabrication experiment.

What started as a frame and engine became a much larger integration project. The photographs follow that progression through the steering mechanism, starter assembly, body panels, and working lights.

### The limitation I would address first

Because braking was electronically commanded, a fault in the control electronics could also remove the brake command. Remote operation was useful for testing, but it did not resolve that dependence. A redesign would need an independent braking provision rather than relying on the same control path as the rest of the vehicle.

The kart was an experimental build, not a validated road vehicle. This is the clearest design limitation I would address before developing it further.

## HURC Mars rover

Building Harvard's Mars rover while mentoring its electrical team and helping develop an onboard soil-sampling and testing module.

**Role:** Vice President; science-module mechanical work, electronics integration, and team mentoring

**Status:** Team rover and science-module integration in progress

### About the University Rover Challenge

The University Rover Challenge is an international student robotics competition held annually in the desert of southern Utah. Teams design and build Mars-rover prototypes for demanding field tasks. Our rover is being developed for that challenge.

### Joining a new team

I joined the Harvard Undergraduate Robotics Club in the spring of my freshman year, when the team was only a few months old and had roughly half a dozen active members. It needed practical help with electronics as much as it needed a finished rover.

My early work included laying out the main electronics assembly and helping integrate components while the arm and chassis were still being developed. I became Vice President that summer and began spending more time on recruiting, training, and coordinating the teams as well as building hardware.

### Developing the onboard science module

Over winter break, I supervised the science team and worked heavily on the module's mechanical design. The intended sequence was to drill below the surface, collect a soil sample from roughly 10 cm down, transfer it to the testing area, and perform measurements onboard.

The module combined drilling and sample handling with chemical and optical testing, plus subsurface humidity and temperature measurements. My contribution was to the mechanical design and integration of that hardware as part of the team effort. The bench photographs show the drilling carriage, wiring, and electronics before complete rover integration.

### Teaching the team that designed the power board

I coached two electrical-team members from relatively little circuit experience through designing the rover's main power-distribution board. They designed the board; my role was teaching, design guidance, and helping them turn that work into a subsystem the rest of the rover could use.

The board brings together fused power distribution and control connections for the rover's motors and science hardware. The assembled photograph shows the connectors, protective fuses, and controller. This is one of the parts of the project I am proudest of, because the outcome was both a piece of hardware and two students who could take ownership of it.

### Growing the club without centralizing every decision

As the rover grew from separate mechanisms into a vehicle, we also had to grow the team. Recruiting, fundraising, and onboarding became substantial parts of my role. I taught CAD and practical circuit-board design and helped organize the work so it did not all depend on a few experienced members.

Lessons from NROTC about clear responsibility and distributed leadership were useful here. The next challenge is continuing to integrate the subsystems while bringing new students into the work. The rover remains an ongoing team project, with science and autonomous-navigation capabilities still being developed and tested.

## Ion-thruster RC boat

An experimental remote-controlled boat propelled by ionic wind, with no moving propulsion parts.

**Role:** Independent project

**Status:** Low-efficiency propulsion demonstrated

### Why I chose a boat

I wanted to explore ionic-wind propulsion without first having to make a vehicle light enough to fly. A floating platform gave me a way to test the thrusters against relatively low resistance while carrying the power supply and radio-control electronics.

The boat used two independently controlled thrusters. Changing the thrust on one side relative to the other let it steer without a rudder or conventional propeller.

### Iterating on the electrodes

I tried several electrode geometries, compared them with designs I had researched, and revised the mounts to make further adjustment possible. The experiment centered on the relationship between the electrode arrangement and the motion of the boat, not on adding more mechanical complexity.

The high-voltage modules also made the difference between an advertised rating and a measured result important. I did not treat the number printed in a product listing as a verified operating voltage.

### What the prototype achieved

The result was a functioning remote-controlled boat with differential steering and no moving propulsion parts. It was not an efficient replacement for a propeller-driven boat, but it gave me a working platform for exploring an unfamiliar propulsion mechanism.

## 3D-printed mechanical clock

A gravity-driven printed clock whose gear and tolerance revisions reduced the required counterweight by 75%.

**Role:** Independent project

**Status:** Working mechanism

### A clock powered by gravity

I designed and printed a fully mechanical clock driven by a hanging weight. A gear train passes the weight's motion to an escapement, the mechanism that releases it in regular steps. The project depended on getting a chain of printed parts to run with very little available energy.

### An escapement and three time scales

I began with the escapement, tuning the geometry so it would both release the gear train in regular steps and keep the pendulum moving. The escape wheel had 60 teeth and also served as the seconds display. A 60:1 reduction connected it to the minute hand, with a further 12:1 reduction for the hour hand.

A hanging weight unwound a spool on the minute-hand shaft to drive the mechanism. I split the pendulum into two parts connected by an adjustment screw, so I could change its effective length and tune the clock's timing after assembly.

### Finding friction in the gear train

The large gear ratio made friction near the escapement particularly costly. A small amount of rubbing at that end of the mechanism could demand a much heavier driving weight.

I printed many variations of the gear geometry and clearances, then checked how the assembled mechanism behaved. The pile of rejected parts was not separate from the design process; it was how I learned which details mattered.

### Reducing the driving weight

The geometry and tolerance changes reduced the required counterweight mass by 75%. The clock was recorded as completed in February 2023. That improvement is the clearest result of the project: a mechanism that needed less driving force after its printed parts were made to work together more efficiently.

## Remote-controlled Hot Wheels

A miniature RC car with diagonally opposed drive motors, reused servo electronics, and a magnetically aligned charging case.

**Role:** Independent project

**Status:** Working prototype

### Making the most of a tiny package

This was one of my favorite early engineering projects. I started by trying to fit motors into an existing Hot Wheels car with a Dremel, then moved toward a custom printed chassis built around a small radio receiver. The project also marked my move from simpler CAD tools toward Onshape.

My teacher explored using a miniature steering linkage. I wanted two drive motors instead, with steering produced by changing the relative speeds of the two sides. That removed the separate steering actuator, but created a difficult packaging problem.

### Reusing the electronics inside a servo

I disassembled small 9 g servos to reuse their motors and control boards. The original feedback arrangement was meant to hold an output position; I adapted it for continuous speed control and used a multi-turn trimmer to set the neutral point. The receiver could then command a motor to turn forward or backward.

Reusing those components let me concentrate on the drivetrain and packaging rather than designing a miniature speed controller from the ground up.

### Driving opposite corners

Both motors were too wide to fit beside one another on the rear axle. I instead drove the rear-left and front-right wheels. That gave the motors separate spaces inside the car while still letting me steer by varying the two wheel speeds.

I printed flexible TPU tires and resin hubs for the driven wheels, with the remaining wheels printed in resin. Small printed gears transferred the motor motion to the wheels. At this scale, small errors in a part or its placement could keep the gears from working together.

### Finishing the car and its case

I adapted a downloaded Dodge Hellcat body to fit the chassis, added LEDs, and powered the car with a small lithium-polymer battery. The finished vehicle was approximately 1.25 times the size of a standard Hot Wheels car. The body model was adapted from an existing design; the drivetrain, packaging, and charging arrangement were my work.

The charging case became part of the project rather than an afterthought. It protected the car and used magnets to line it up with the charging contacts. Taking the project from a miniature drivetrain to a car with its own case was a large part of why I enjoyed it.

## Automated hydroponic grow farm

An automated home growing system, from a small lettuce bed to shelves of microgreens.

**Role:** Independent project

**Status:** Built and used

### A growing system I could build at home

A Popular Mechanics article about hydroponics made me want to try growing food without soil. I started with lettuce, researched different watering approaches, and chose a simple system I could build from plastic tubs, a pump, lights, and a shelf.

Mechanical timers controlled the early watering and lighting cycles. One version used a concrete-mixing tub as the grow bed. The interesting part was connecting a simple control system to something that needed the right conditions even when I was not there to tend it.

### Scaling to microgreens

In the later version, I moved to microgreens and built pine shelving to hold multiple trays. Newly planted trays spent several days in a dark incubation box before moving to the growing shelves. An Arduino controlled watering and the LED lights followed a 16-hour daylight cycle.

The shelves could hold batches at different stages of growth. That made the layout and schedule as important as any individual pump or light.

### A system that had to keep running

The work combined carpentry, plumbing, electronics, and a repeatable growing process. It was one of my early experiences with automation outside a classroom demonstration: the plants still needed the right conditions when I was doing something else.

### Trying different scales

I experimented with both larger plants and trays of microgreens, and built a smaller home setup for a child in my neighborhood using inexpensive wood and other materials. Making more than one version helped me separate the basic growing process from the particular size or shape of the shelving.

## Low-cost RC plane

A low-cost foam aircraft developed through repeated redesigns, repairs, and flight tests.

**Role:** Independent project

**Status:** Flight demonstrated

### Learning through successive airframes

I began experimenting with low-cost remote-controlled aircraft in 2017, with very little engineering experience. I tried foam board, cardboard, an adapted foam aircraft, a delta-wing layout, and eventually a larger airframe made from insulation foam. Using inexpensive materials meant a crash did not have to end the project.

I used radio control and servo-operated surfaces, with an onboard camera in later versions. I also experimented with assisted takeoff. The individual airframes changed, but the project stayed with me for years.

### Build, fly, repair, repeat

Some airframes were repaired and flown repeatedly before I retired the design. Others led to a different configuration. The photos include damaged aircraft as well as finished ones because the repairs and unsuccessful flights were a substantial part of the work.

My earlier project log records a successful flight in June 2023. That came after years of attempts, rather than after one clean design-and-build cycle.

### What stayed with me

This was one of the first projects that taught me to keep returning to a difficult problem after a disappointing test. A CAD model could look convincing, but the actual airframe still had to fly. Keeping the builds inexpensive and repairable gave me more chances to learn from what happened outside.

## Hybrid RC car

An electric-drive and automatic-start conversion for a Traxxas nitro RC car.

**Role:** Independent project

**Status:** Starter demonstrated

### A small version of a car I loved

After learning to drive in a Toyota Highlander Hybrid, I wanted to explore combining an electric motor and combustion engine on a much smaller scale. My engineering teacher gave me a nitro RC car, which became the starting point.

I added electric drive so the car could be operated electrically, with its original engine, or with both power sources. Working around an existing chassis made packaging and the connection to the original drivetrain central parts of the project.

### Adding an electric starter

I also added a DC motor to start the nitro engine remotely. The linked demonstration shows that starter operating. These controls drew on the radio-control work I had already done for other vehicles, but the engine introduced a different starting and mechanical-integration problem.

The project was a working conversion, not a controlled comparison of fuel consumption or efficiency. Its value was in making the two power sources and starting system work together in a compact vehicle.

## Industrial robotic vacuum

A workshop-cleaning robot with a custom cyclone vacuum, a repurposed mobile base, and ultrasonic wall-following.

**Role:** Independent project

**Status:** Built and operated; distance-sensor reliability limited navigation

### A practical problem in the workshop

Our school engineering space was often messy, and the robot vacuum at home made me wonder whether I could build a larger version for the room. I started with a rolling trash-can base and added two large DC motors with VersaPlanetary gearboxes. A rear caster balanced the chassis.

An Arduino controlled the two motor drivers. Reusing the base let me focus on the drive system, vacuum hardware, and behavior instead of fabricating every part of the chassis.

### Building the vacuum, not just the robot

I designed a custom impeller and a printed cyclone assembly rather than attaching a complete commercial vacuum. The cyclone used rotating airflow to separate debris into the collection chamber. This made airflow and mechanical fabrication substantial parts of the project alongside the mobile platform.

### Teaching it to move around the room

Ultrasonic sensors measured the distance to nearby walls. I programmed behavior based on what I had observed in the vacuum at home: move through the room, turn when encountering a wall, and follow the wall until it ended. This was a simple sensor-driven routine, not a map of the entire room.

The robot drove and operated its vacuum, but unreliable ultrasonic readings made the navigation inconsistent. A different distance-sensing approach would be one of my first changes in a new version.

## Universal arcade cabinet

A Raspberry Pi arcade cabinet built with my brother from inexpensive wood and a reused monitor.

**Role:** Built with my brother; cabinet design adapted from YouTube

**Status:** Completed and playable

### Building something with my brother

My brother and I made an arcade cabinet from inexpensive wood and a repurposed computer monitor. This project used a cabinet design we found on YouTube, rather than being an original design of mine. Our work was the fabrication, control-panel assembly, wiring, and setup.

### Turning buttons into game controls

We drilled the control panel for joysticks and buttons and wired them into an IPAC 4 interface. That board translated button presses into keyboard inputs for the Raspberry Pi inside the cabinet. The photos show the enclosure before the screen and controls were fitted, along with the underside of the completed panel.

### From a pile of materials to a playable cabinet

The project combined carpentry and electronics in a machine we could actually use together. It was completed by March 2022, and the video shows Asteroids running on the finished cabinet.

## Two-axis thrust-vector gimbal

A printed pitch-and-yaw gimbal and an early lesson in designing for the operating environment.

**Role:** Independent project

**Status:** Prototype ended after damage during its first ground test

### A two-axis mechanism

For an early rocket project associated with my calculus class, I designed a gimbal with two nested axes. Small actuators changed its pitch and yaw. The CAD model and prototype photos show the moving rings and their mounts.

My focus was the mechanism: obtaining controlled angular movement in two directions within a compact assembly.

### What the first test exposed

I fixed the rocket body to a ground-test mount to try the two axes. The prototype was destroyed during the first firing test when continued burning damaged the printed structure. I did not continue the project after that test.

The mechanism was a prototype, not a demonstrated guidance system or a successful controlled flight. A working motion model was not enough: the structure also had to tolerate the environment in which it would operate.

## Lab parts and equipment database

A searchable directory for the components and test instruments in the Rowland electronics lab.

**Role:** Research assistant, Rowland Institute

**Status:** Directory interface documented

### Finding what the lab already has

I worked on a parts and equipment database for the Rowland electronics lab. A useful component is only useful if someone can find it: the lab has shelves of boxed parts as well as racks of test instruments, so organizing those two kinds of inventory was the starting point.

### One entry point for parts and instruments

The browser-based directory separates component search from the instrument database. It gives the lab a single place to start looking, whether the need is a small electronic part or a piece of test equipment.

The interface shown here is the actual Rowland E.E. Lab Inventory Directory. The accompanying photos show the component storage and instrument racks it was built around.

### Software as a laboratory tool

This was a different kind of instrumentation work: helping people locate the hardware needed to run an experiment. It connected software to the organization of a working lab, where components and equipment have to remain findable as projects change.

## Geophone vibration test stand

An electromagnetic test stand that replaced a noisy eccentric-shaft mechanism with a hand-wound actuator and tuned printed springs.

**Role:** Mechanical mounts and test-stand design; logger electronics by Winfield Hill

**Status:** Electromagnetic test-stand prototype built and operated

### A test stand for a very sensitive instrument

Winfield Hill had developed the electronics for vibration recorders used around electron microscopes and other laboratory equipment. My work was to build the mechanical sensor mounts and create a test stand for comparing the recorders.

The stand needed controllable motion of roughly 0.1 mm and a way to test each of the three sensing directions. That amplitude was awkward: it was much smaller than the motion I could conveniently obtain from conventional mechanisms, yet larger than the very small displacements I associated with other actuator approaches.

### Why the eccentric-shaft version failed

I first tried generating vibration with an eccentric shaft in a printed mechanism. The intended motion was present, but vibration from the rest of the mechanism was larger than the signal I wanted to create. Changing the eccentricity would not solve the underlying problem: the test apparatus itself was dominating the measurement.

I needed a simpler way to apply force to the sensor carriage, with fewer sources of unwanted mechanical motion.

### Designing an electromagnetic alternative

Drawing on the printed-motor work from my e-bike project, I printed a magnetic core and wound a coil around it by hand. Permanent magnets on the moving mount interacted with that coil, while linear guides allowed the carriage to move relative to the base.

The fixture let a recorder clip into place in each of the three required orientations. I supported the moving assembly with printed springs and estimated their stiffness using hand calculations and finite-element analysis. The spring stiffness and moving mass had to be chosen together, rather than treating the spring as a generic part.

### Checking the structure and operating the stand

I drove the actuator with amplifiers supplied by the lab. Compared with the eccentric-shaft version, the electromagnetic arrangement had fewer moving parts and was easier to control.

I also analyzed the sensor mount's frequency response. The simulation showed a first significant amplification mode near 3.8 kHz, beyond the useful few-hundred-hertz range discussed for the geophones. That was a structural simulation result, not a measured bandwidth specification for the complete test stand. The useful outcome was the quieter, more controllable test mechanism and a better understanding of how the fixture could affect the measurement.

## 64-element directional sound array

A custom ultrasonic array that demonstrated directional audible output, with tests that exposed limits in the original control architecture.

**Role:** Independent project

**Status:** Directional output demonstrated

### A compact, directional source of sound

For Physics 15C, I wanted to turn our work on waves and interference into a directional sound source. A compact array working directly at audible frequencies would not give me the narrow beam I wanted, so I investigated an ultrasonic approach using an 8 by 8 array of 64 transducers around a 40 kHz carrier.

The project also explored audible tones produced using nearby ultrasonic frequencies and the nonlinear response of the medium. The goal was not simply a louder speaker, but sound that was much more concentrated in one direction.

### Simplifying 64 independent channels

The intended controller needed to set the timing of every transducer. I designed around an STM32F103, eight addressable latches, and a counter so I could update groups of outputs instead of assigning a separate processor output to each element.

I also took advantage of the transducers' narrow frequency response. The proposed driver used square-wave switching and a simple MOSFET-and-resistor circuit for each element, rather than a separate sine-wave generator for every channel. The latches were meant to retain each output state between updates.

A receiver using additional transducers, filters, and comparator inputs was a planned extension for time-of-arrival measurements. It was not a completed ranging demonstration.

### Changing the test when the controller became the obstacle

A problem in the latch architecture prevented the full per-element control from working as intended. For the documented experiments, I split the array into two banks of 32 transducers and drove them with two function generators.

This simpler setup let me test the acoustic behavior without waiting for the complete timing system. The experiments used a 30 V bench supply and investigated audible envelopes at 440 Hz and 1 kHz.

### Measuring the beam

I measured sound level as the measurement direction moved from 0 to 90 degrees in 5-degree steps, repeating the measurements at different distances. The results showed a strong central beam, along with additional off-axis lobes. Reflections could make an object in the beam appear to be the sound source.

The project analysis connected the extra lobes to element spacing and the square array geometry. It also identified an experimental limitation: the two frequency tests used different orientations and noise environments, making direct comparisons less clean than intended.

### What worked, and what remained

The simplified two-bank setup demonstrated directional audible output. Full independent phase control, the receiver, and complete mechanical integration remained unfinished in those experiments. The controller architecture was an important part of the design, but it was not the configuration that produced the documented beam measurements.

The project also led to new work in the Rowland lab: adapting the transducer-array idea for a time-of-flight temperature-measurement instrument at Rubin Observatory. That instrument has a different purpose from the audible-sound demonstration.

## 500 V laboratory power supply

A 300-500 V adjustable laboratory supply combining a custom PCB, hand-wound inductors, and a digital voltage readout.

**Role:** Research assistant, Rowland Institute

**Status:** Prototype bench-tested

### A power supply for vacuum-tube work

A researcher at the Rowland Institute needed an adjustable supply for vacuum-tube work, and we did not have a suitable one on hand. I worked on a boost-converter supply covering 300 to 500 V, including its circuit board and custom-wound inductors.

A voltage readout and output adjustment were part of turning the circuit into an instrument someone could use at the bench.

### Learning by winding the magnetic components

Winding the inductors myself made their behavior a design problem rather than a fixed catalog specification. I worked on inductance, Q, and the core air gap, while also considering energy storage and insulation between windings.

The high operating voltage made the physical arrangement particularly important. I had to think about the winding construction and insulation at the same time as the electrical values, then carry those decisions into the assembled board.

### Board layout and bench testing

The gallery follows the work from schematic and PCB layout to wound components and assembled prototypes. One load-test photograph shows approximately 499 V at 0.100 A, close to the 500 V, 50 W design point.

That was an operating point, not the end of development. The same progress record identifies a problem area on the board. I continued treating component placement, high-voltage construction, and the surrounding instrument hardware as part of the design rather than assuming that obtaining the desired voltage meant the project was finished.

### What the project added to my experience

This work gave me hands-on experience with magnetics and high-voltage instrumentation beyond the motor controllers I had built independently.

## ES51 Turf Wars robot

A six-wheel course robot with a compliant two-speed shifter and an extended-reach arm, built for Turf Wars.

**Role:** Team project; my focus was drivetrain, shifting mechanism, and arm design

**Status:** Competed; drivetrain worked, but arm friction ended our run in the first round

### About Turf Wars

Turf Wars is the robot competition associated with Harvard's ES51 course. Teams design, build, and test remote-controlled machines for a game whose challenge changes between offerings. Harvard SEAS introduces the competition in the video linked below.

### Starting with the game, not an existing robot

For ES51, Computer-Aided Machine Design, our team built a robot for Turf Wars. Our version of the game involved placing objects onto a tic-tac-toe grid. I started by studying the course and asking which design choices would make a practical difference: climbing, turning on turf, and reaching the center of the board.

I wanted to try a different drivetrain and a longer-reaching arm, rather than simply repeating the mechanism we had built in earlier labs.

### A two-speed gearbox with a compliant shifter

I designed a custom gearbox with printed components and metal shafts, paying particular attention to how the parts were located relative to one another. It had a lower ratio for climbing and a higher-speed setting for level ground.

A servo operated the shifting mechanism. Because the two sides of the robot would not necessarily engage their gears at exactly the same moment, the shifter needed compliance: one side could finish engaging while the other was still aligning. In practice, the high-speed setting was too fast to control comfortably, so we used the lower-speed setting throughout the competition.

### Making tank steering easier on turf

I used three wheels on each side, connected by belts. The center wheel sat roughly half an inch lower than the two outer wheels. On the turf, that concentrated more of the load near the middle of the robot and made it easier to turn.

The resulting drivetrain was quick and maneuverable in the low-speed setting. It was the part of the design that held up well during the competition.

### Reaching the center of the grid

I wanted the pickup arm to reach farther than a conventional four-bar linkage, so I designed an extending eight-bar mechanism. Its extra reach was intended to let us place a game piece in the center square.

The acrylic linkage introduced more friction than I had allowed for, and I did not leave enough time to test the assembled arm. Although the drivetrain performed well, the arm did not operate consistently and we lost in the first round.

The lesson was not that an ambitious mechanism is always wrong. It was that I needed to budget time for the difficult part of the design to be built, tested, and simplified if necessary.

## ES125 egg-drop mechanism

A shaped-slot damping mechanism for an egg-drop challenge. Our team placed second, while testing exposed a critical carriage-constraint problem.

**Role:** Team project with Anna Burgess and Justice Hickman-Maynard; my focus was the guide profile and mechanism

**Status:** Second place out of about 50 teams; carriage rotation caused friction and jamming

### Moving beyond a search for spring and damper values

For ES125, Anna Burgess, Justice Hickman-Maynard, and I designed an egg-drop mechanism called M.O.D.E. The challenge was to slow a loaded carriage without breaking the egg, subject to limits on the overall mechanism.

We first tried computational searches over combinations of masses, springs, and dampers. After mixed results, I changed the approach: start from the deceleration history we wanted, then work backward to the geometry that could produce it.

### Shaping the motion to shape the force

Using the specified drop height, carriage mass, and available travel, I considered a constant-deceleration trajectory. I wrote equations for a pin-and-slot mechanism that changed how quickly the dampers compressed as the carriage moved down the frame.

The slot angle changes the relationship between carriage movement and damper movement. I used that relationship to solve for a guide profile intended to keep the retarding force approximately constant. We modeled the profile in Python, brought it into CAD, and laser-cut the resulting geometry.

### From the ideal curve to a real assembly

The design used eight dampers in parallel, a 1.05 kg carriage, and a frame with four tall guides. The final modeled configuration in our presentation did not include springs.

The CAD walkthrough shows the carriage, frame, and damper arrangement; the photographs show the physical laser-cut structure. The video is a model walkthrough, not footage of a drop test.

### A second-place result and an incomplete constraint

Our team finished second out of about 50 groups. The important mechanical problem was that the upper carriage could rotate away from its intended alignment. That increased friction between the pins and slots and could make the carriage jam.

My model had assumed that friction there would be small. The physical assembly showed why that assumption was not enough: the top platform also needed to be constrained against the unwanted rotation. That would be my first mechanical change in a revised design.

## Smart home controller

A wall-mounted touchscreen controller that opened my shades, ramped up the lights, and made the morning alarm harder to ignore.

**Role:** Independent project

**Status:** Built and installed

### A morning routine designed around light

I wanted an easier way to wake up for school during dark Boston winters. A normal alarm did not address the room itself, so I set out to control the shades and lights as part of the wake-up routine.

The touchscreen went across the room, in a housing designed around the existing light-switch location. Its position was deliberate: turning off the final alarm would require getting out of bed.

### Using the CNC to iterate on the electronics

I had recently finished my homemade PCB mill, which let me make and revise the controller boards quickly. The later controller brought together an Arduino, a real-time clock, a touchscreen, lighting control, and motorized shades.

I designed the enclosure and the small shade mechanisms, routed the low-voltage wiring, and wrote the touchscreen interface myself. The UI let me switch individual devices, change settings, and set alarms. The work tied together a custom circuit board, mechanical actuators, and software in something I could use every day.

### Making it difficult to stay in bed

The routine began about 20 minutes before the alarm, opening the shades and gradually bringing up the lights to simulate a sunrise. If I was still in bed five minutes after the intended wake-up time, the LED lighting began flashing and the audible alarm made the room much harder to ignore.

To stop it, I had to walk across the room and hold a finger on the touchscreen for ten seconds. That interaction was as important as the hardware: the system was designed around getting me out of bed, not just sending another notification.

### A personal installation

The controller was built and installed in my room. It included switching for the existing room lights as well as low-voltage devices; it was a personal prototype, not a certified or packaged home-automation product. The photographs show the progression from exposed prototype wiring to the mounted display and enclosure.
