// PM2 Ecosystem Configuration with Watchdog
// Includes watchdog process for health monitoring

module.exports = {
  apps: [
    // Main services
    {
      name: 'orchestrator',
      script: 'venv/bin/python',
      args: 'scripts/run_ai_employee.py --daemon --interval 300',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/orchestrator-error.log',
      out_file: 'logs/orchestrator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'gmail-watcher',
      script: 'venv/bin/python',
      args: 'scripts/gmail_watcher.py --continuous --interval 300',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/gmail-watcher-error.log',
      out_file: 'logs/gmail-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'whatsapp-watcher',
      script: 'venv/bin/python',
      args: 'scripts/whatsapp_watcher.py --continuous --interval 120',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/whatsapp-watcher-error.log',
      out_file: 'logs/whatsapp-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'linkedin-watcher',
      script: 'venv/bin/python',
      args: 'scripts/linkedin_watcher.py --continuous --interval 300',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/linkedin-watcher-error.log',
      out_file: 'logs/linkedin-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'reply-generator',
      script: 'venv/bin/python',
      args: 'scripts/reply_generator.py --continuous --interval 300',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/reply-generator-error.log',
      out_file: 'logs/reply-generator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'reply-sender',
      script: 'venv/bin/python',
      args: 'scripts/reply_sender.py --continuous --interval 600',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/reply-sender-error.log',
      out_file: 'logs/reply-sender-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },
    {
      name: 'ralph-wiggum',
      script: 'venv/bin/python',
      args: 'scripts/ralph_wiggum_loop.py continuous',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '400M',
      env: {
        DISPLAY: ':99',
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/ralph-wiggum-error.log',
      out_file: 'logs/ralph-wiggum-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 5000
    },

    // System Health Watchdog
    {
      name: 'watchdog',
      script: 'venv/bin/python',
      args: 'watchdog.py',
      cwd: process.env.PWD || process.cwd(),
      interpreter: 'none',
      autorestart: true,
      watch: false,
      max_memory_restart: '200M',
      cron_restart: '*/5 * * * *',  // Run every 5 minutes
      env: {
        PYTHONUNBUFFERED: '1'
      },
      error_file: 'logs/watchdog-error.log',
      out_file: 'logs/watchdog-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss',
      merge_logs: true,
      min_uptime: '5s',
      max_restarts: 5,
      restart_delay: 10000
    }
  ]
};
