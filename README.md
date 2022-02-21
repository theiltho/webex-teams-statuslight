# webex-teams-statuslight

This is a small project for creating a diy busylight for cisco webex teams. Inspired by https://github.com/matthewf01/Webex-Teams-Status-Box

I used three LEDs, a Raspberry B Rev 2 and a random box.

## Installation

### Hardware

To get an idea how the wiring works you can read [this article](https://www.instructables.com/Raspberry-Pi-3-RGB-LED-With-Using-PWM/).

Make sure to use the correct pin numbers https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header

### Software

You will need 2 pieces of information to complete software setup:

1. Your bot's access token from Webex:
create a bot at the site below. Give it a unique name and you'll get an access token https://developer.webex.com/my-apps/new/bot

2. Your user's personId from Webex: https://developer.webex.com/docs/api/v1/people/get-my-own-details 
Sign into your Webex account, then under the "Try It" section, click "Run"; Copy the value id from the response shown

Now update the file `webexteams.service` file with your token and id and install it as a service:

```bash
sudo mv webexteams.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable webexteams.service # optional; see cronjob below
```

**Start/Stop/Status**: `sudo systemctl {status|start|stop} webexteams.service`

#### Cronjob

The service does not need to be running at night or at the weekend so I created a cronjob:

```
# 8:01 am Mon-Fri start
1 8 * * 1-5 systemctl start webexteams.service >/dev/null 2>&1
# 19:01 Mon-Fri stop
1 19 * * 1-5 systemctl start webexteams.service >/dev/null 2>&1
```

## Troubleshooting/Debugging

- What status do the LEDs currently have? Again, replace the numbers with your actual pins.
    ```bash
    $ raspi-gpio get | egrep "(GPIO 4:|GPIO 18:|GPIO 25:)" | awk '{print $1 " " $2 " " $3}'
    GPIO 4: level=0
    GPIO 18: level=0
    GPIO 25: level=1 # white LED is currently active
    ```

- Set the pins manually:

    ```bash
    $ raspi-gpio set 1 op dh # sets gpio pin 1 on
    $ raspi-gpio set 1 op dl # sets gpio pin 1 off
    ```

- Logging

  `std_err` is logged to `/home/pi/webex-teams-statuslight/webexstatus_err.log` (change the location in the service file). There is no log to `std_out` but you can enable it also within the service file.
  
- Documentation: https://webexteamssdk.readthedocs.io/en/latest/index.html
