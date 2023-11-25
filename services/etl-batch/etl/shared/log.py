import logging
from datetime import datetime


def create_logger():
    logger = logging.getLogger("sequence_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def time_it_seq(name: str, logger: logging.Logger):
    def sequence_decorator(sequence: callable):
      def sequence_wrapper(*args, **kwargs):
          logger.info(f"Starting Pipeline Sequence: '{name}'.")

          start_tm = datetime.now()
          result = sequence(*args, **kwargs)
          end_tm = datetime.now()
          duration = (end_tm - start_tm).total_seconds()
          
          logger.info(f"Start Time: {start_tm.strftime('%Y-%m-%d %H:%M:%S')}")
          logger.info(f"End Time: {end_tm.strftime('%Y-%m-%d %H:%M:%S')}")
          logger.info(f"Finish Pipeline Sequence: '{name}'. Elapsed time: {time_fmt(duration)}.")
          return result
      return sequence_wrapper
    return sequence_decorator

def time_fmt(total_seconds: int) -> str:
    days = time_fmt_cd((total_seconds // 86400), "day")
    hours = time_fmt_cd(((total_seconds % 86400) // 3600), "hour")
    minutes = time_fmt_cd(((total_seconds % 3600) // 60), "minute")
    seconds = time_fmt_cd(round((total_seconds % 60), 2), "second")

    time_fmt_join = ", ".join([
        tm
        for tm in [days, hours, minutes, seconds]
        if (tm)
    ])
    return time_fmt_join


def time_fmt_cd(tm: int, label: str):
    if (tm):
        fmt_label = label + 's' if (tm > 1) else label
        fmt_time = f"{tm} {fmt_label}"
        return fmt_time
