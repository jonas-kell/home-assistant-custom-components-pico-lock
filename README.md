# HomeAssistant Custom Components Pico Lock

Pico-driven Lock Integration. Install it via HACS.
Used to talk to a RaspberryPi Pico running the custom micropython code also contained in this repo.
The Pico then is used to control a lock over GPIO.
This at the moment only assumes that a pull-down of one GPIO pin triggers the opening of a lock temporarily and afterwards it closes on its own.
Doesn't track open-state of the lock or support manually closing.

## To use the Pico-Dev-Environment (VS-Code):

-   Install all the extensions mentioned in `.vscode/extensions.json` (VSCode should automatically prompt you to do this)
-   Run the Command `Pico-W-Go > Configure project`
-   Connect to a "Raspberry-Pi-Pico W" that has [Micropython](https://micropython.org/) firmware already flashed ([How to do this](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython)) to serial USB
-   Move the `pi_config.env.example` to `pi_config.env` and fill in the settings
-   Run the command `Pico-W-Go > Upload Project to Pico`
-   The pico should now be operational. Try disconnecting it and connect it to a power supply. The LED should flash one indicating boot and a second time indicating network status
    -   If the second flash is a singular flash, it did not manage to connect to the wifi you specified
    -   If the second flash is a double flash, it managed to connect to the wifi. Look into your Router to find out its IP-Address

## Hacs Integration

Example `configuration.yaml` entry

```
lock:
    - platform: pico_lock
      devices:
          my_lock:
              name: My Pico Lock
              ip_address: 192.168.2.XXX
```

-   `name`: Name duh
-   `ip`: The IP-Address that is used to talk to the pico (get it from your router, ideally set it to be static)
