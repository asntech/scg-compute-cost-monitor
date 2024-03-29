# SCG compute cost monitor
> Track your group's monthly compute charges per user and ring the alarm if costs exceed the limit

## Description
The bash script `scg_compute_cost_monitor` calculates the monthly CPU cost for a specified lab group on the Stanford's [SCG](https://login.scg.stanford.edu/) HPC cluster. It allows users to monitor their compute costs and optionally receive email alerts if the cost exceeds a specified monthly limit. The script includes logging functionality to prevent repeated email notifications for users who have already been notified within the same month.

## Usage
Before using the script, ensure you've access to the [SCG cluster](https://login.scg.stanford.edu/) and you are on cluster.

**Get the script**: Obtain the `scg_compute_cost_monitor` script and ensure it is executable.

```bash
git clone https://github.com/asntech/scg-compute-cost-monitor.git
cd scg-compute-cost-monitor
chmod +x scg_compute_cost_monitor
```
**Run the script**: Execute the script from the terminal with appropriate options to calculate the monthly CPU cost for your lab group. Try `-h` argument to see the options.

```
./scg_compute_cost_monitor -h

Usage: ./scg_compute_cost_monitor [-m <month>] [-y <year>] -a <pi_sunet> [-l <monthly_limit>] [-e <send_email>] [-c <cc_email>]

Options:
  -m <month>: Specify the month (default: current month)
  -y <year>: Specify the year (default: current year)
  -a <pi_sunet>: Specify the PI SUNet ID (required)
  -l <monthly_limit>: Specify the monthly cost limit (default: 800)
  -e <send_email>: Specify whether to send email alerts for exceeding the limit (set to: true)
  -c <cc_email>: Specify email addresses to cc the alerts (optional)
  -d <log_dir>: Path to store log files for email alerts (optional)"
  -h: Display this help message

  ```

The script will display the CPU hours and charges for each user in the specified lab group for the specified month and year.

*Email alerts*: If the cost exceeds the specified monthly limit and send_email is set to true [`-e true`], email alerts will be sent to the respective users. Optionally, you can specify email addresses to cc the alerts using the `-c <cc_email>` option. The script logs the users who have been notified in a log file to prevent repeated notifications within the same month. You can change the log directory path by setting `-d` argument.

## Example

Get CPU usage/cost report for each user associated PI account. This command will calculate the monthly CPU cost for lab group in March 2024. You can skip `-y` and `-m` to get the report for the current month. 

```
./scg_compute_cost_monitor -a PI_SUNetID -m 03 -y 2024
```

To get the report but also send an alert email to those users with monthly compute cost limit is above $1000 in the current month. 
```
./scg_compute_cost_monitor -a PI_SUNetID -l 1000 -e true -c <cc_email>@stanford.edu
```
If the cost exceeds 1000 USD, email alerts will be sent to your `SUNet@stanford.edu` and can optionally cc to you PI or lab admin `<cc_email>@stanford.edu`. The script will prevent repeated email notifications for users who have already been notified within the same month.

## Automating the process with Cron Jobs
To automate the execution of the script periodically, you can utilize cron jobs. Cron is a time-based job scheduler in Unix-like operating systems, which allows you to schedule tasks to run at fixed intervals. Here's how you can set up a cron job to run the script periodically:

SSH into SCG cluster where you need to schedule the cron job.
First create a bash script to source `.bashrc` and run the `scg_compute_cost_monitor` script
```bash
vim run_scg_compute_cost_monitor.sh
```

Add these lines to the script and update the path and arguments
```
#!/bin/bash
source ~/.bashrc

# run the compute monitor script
/path/to/scg-compute-cost-monitor/scg_compute_cost_monitor -a <pi_sunet> -l <monthly_limit> -e true -c <cc_email>
```
Replace <pi_sunet>, <monthly_limit>, and can also add <cc_email> with the desired values for the script's options.

Make the script execuitable:
```
chmod +x /path/to/run_scg_compute_cost_monitor.sh
```

Now edit the crontab file by running the command:

```bash
crontab -e
```

Add a new line to the crontab file with the following format:

```bash
30 09 * * * /path/to/run_scg_compute_cost_monitor.sh
```

This line specifies that the script should run every day at 09:30am in the morning.
Replace /path/to/run_scg_compute_cost_monitor.sh with the actual path to your script.

Save the crontab file and exit the editor.

Now, the cron job is scheduled to execute the script automatically at the specified time intervals. You can adjust the cron schedule according to your requirements by modifying the timing values (e.g., minute, hour) in the cron job line.

**Note:** Make sure that only one person schedules the cron job in your group to avoid multiple alerts.


## Get a month report

To get yearly SCG compute cost report for your lab you can use `scg_compute_cost_report.py`. This Python script generates a yearly SCG compute cost report and also provides an option to plot the per-month cost and user usage plots.


Firt you need to load the `Python v3.11.1` or install python packages using `pip install -r requirements.txt`

```
module load python/3.11.1
```
And try the help.

```
$ scg_compute_cost_report.py --help

Usage: scg_compute_cost_report.py [OPTIONS]

  Get yearly SCG compute cost report for your lab

Options:
  -a, --account TEXT  PI SUNet ID  [required]
  -y, --year INTEGER  Year (default: current year)
  -b, --bin PATH      Binary file path  [default: scg_compute_cost_monitor; required]
  -p, --plot          Plot the usage stats
  -o, --outdir PATH   Output path  [required]
  --help              Show this message and exit.
```

### Example usage

```
python scg_compute_cost_report.py -a <account_id> -y 2023 --plot -o <output_directory>
```