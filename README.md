# SCG Compute Cost Watchdog
> Track your group's monthly charges per user and ring the alarm if costs exceed the limit

## Description
This is a Bash script created to calculate the monthly CPU cost for a specified lab group on the Stanford's [SCG](https://login.scg.stanford.edu/) HPC cluster. It allows users to monitor their compute costs and optionally receive email alerts if the cost exceeds a specified monthly limit. The script includes logging functionality to prevent repeated email notifications for users who have already been notified within the same month.

## Prerequisites
Before using the script, ensure the following :
- You've access to the [SCG cluster](https://login.scg.stanford.edu/)
- And you can run `get_compute_charges` command-line tool

## Usage
**Get the script**: Obtain the `scg_compute_cost_watchdog` script and ensure it is executable.

```bash
git clone https://github.com/asntech/scg-compute-cost-watchdog.git
cd scg-compute-cost-watchdog
chmod +x scg_compute_cost_watchdog
```
**Run the script**: Execute the script from the terminal with appropriate options to calculate the monthly CPU cost for your lab group. Try `-h` argument to see the options.

```
./scg_compute_cost_watchdog -h

Usage: ./scg_compute_cost_watchdog [-m <month>] [-y <year>] -p <pi_sunset> [-l <monthly_limit>] [-e <send_email>] [-c <cc_email>]

Options:
  -m <month>: Specify the month (default: current month)
  -y <year>: Specify the year (default: current year)
  -a <pi_sunset>: Specify the PI sunset ID (required)
  -l <monthly_limit>: Specify the monthly cost limit (default: 800)
  -e <send_email>: Specify whether to send email alerts for exceeding the limit (set to: true)
  -c <cc_email>: Specify email addresses to cc the alerts (optional)
  -h: Display this help message

  ```

The script will display the CPU hours and charges for each user in the specified lab group for the specified month and year.

*Email alerts*: If the cost exceeds the specified monthly limit and send_email is set to true [`-e true`], email alerts will be sent to the respective users. Optionally, you can specify email addresses to cc the alerts using the `-c <cc_email>` option. The script logs the users who have been notified in a log file to prevent repeated notifications within the same month. You can change the log directory path by setting `LOG_DIR` variable in the script.

## Example

```
./scg_compute_cost_watchdog -a PI_SUNetID -m 03 -y 2024 -l 1000 -e true -c PI_SUNetID@stanford.edu
```

This command will calculate the monthly CPU cost for lab group in March 2024. If the cost exceeds 1000 USD, email alerts will be sent to your `SUNet@stanford.edu` and cc'd to `PI_SUNetID@stanford.edu`. The script will prevent repeated email notifications for users who have already been notified within the same month. To get the current month, you don not need to set `-m` and `-y` arguments.

## Automating the process with Cron Jobs
To automate the execution of the script periodically, you can utilize cron jobs. Cron is a time-based job scheduler in Unix-like operating systems, which allows you to schedule tasks to run at fixed intervals. Here's how you can set up a cron job to run the script periodically:

SSH into SCG server where you need to schedule the cron job.

Edit the crontab file by running the command:

```bash
crontab -e
```

Add a new line to the crontab file with the following format:

```bash
0 0 * * * /path/to/scg_compute_cost_watchdog -a <pi_sunset> -l <monthly_limit> -e true -c <cc_email>
```

This line specifies that the script should run every day at midnight (00:00).
Replace /path/to/your/script.sh with the actual path to your script.
Replace <pi_sunset>, <monthly_limit>, and can also add <cc_email> with the desired values for the script's options.

Save the crontab file and exit the edit or.

Now, the cron job is scheduled to execute the script automatically at the specified time intervals. You can adjust the cron schedule according to your requirements by modifying the timing values (e.g., minute, hour) in the cron job line.

**Note:** Make sure that only one person schedules the cron job in your group to avoid multiple alerts.

