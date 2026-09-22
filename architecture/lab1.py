import platform
import socket

import psutil
import typer


LABEL_WIDTH = 28


def gb(value: int) -> str:
    return f"{value / 1024**3:.2f} ГБ"

def title(text: str) -> None:
    typer.secho(f"\n{text}", fg=typer.colors.CYAN, bold=True)

def info(label: str, value, color: str = typer.colors.WHITE) -> None:
    typer.echo(f"{label:<{LABEL_WIDTH}}", nl=False)
    typer.secho(str(value), fg=color, bold=True)

def main() -> None:
    typer.secho(
        "\nИНФОРМАЦИЯ О КОМПЬЮТЕРЕ",
        fg=typer.colors.MAGENTA,
        bold=True,
    )

    title("ОПЕРАЦИОННАЯ СИСТЕМА")

    info("Система", platform.system(), typer.colors.CYAN)
    info("Версия", platform.release())
    info("Архитектура", platform.machine())
    info("Имя компьютера", socket.gethostname())

    title("ПРОЦЕССОР")

    info(
        "Процессор",
        platform.processor() or "Не определён",
        typer.colors.BLUE,
    )
    info("Физические ядра", psutil.cpu_count(logical=False))
    info("Логические ядра", psutil.cpu_count(logical=True))
    info(
        "Загрузка",
        f"{psutil.cpu_percent(interval=0.5):.1f}%",
        typer.colors.GREEN,
    )

    title("ОПЕРАТИВНАЯ ПАМЯТЬ")

    memory = psutil.virtual_memory()

    info("Общий объём", gb(memory.total))
    info("Используется", gb(memory.used), typer.colors.YELLOW)
    info("Доступно", gb(memory.available), typer.colors.GREEN)
    info("Загрузка", f"{memory.percent:.1f}%", typer.colors.CYAN)

    title("НАКОПИТЕЛИ")

    for partition in psutil.disk_partitions():
        try:
            disk = psutil.disk_usage(partition.mountpoint)
        except (PermissionError, OSError):
            continue

        typer.echo()

        info("Устройство", partition.device, typer.colors.BLUE)
        info("Точка подключения", partition.mountpoint)
        info("Файловая система", partition.fstype or "Неизвестно")
        info("Общий объём", gb(disk.total))
        info("Используется", gb(disk.used), typer.colors.YELLOW)
        info("Свободно", gb(disk.free), typer.colors.GREEN)
        info("Заполнение", f"{disk.percent:.1f}%", typer.colors.CYAN)

    title("СЕТЬ")

    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for name, addresses in interfaces.items():
        ipv4 = ipv6 = mac = None

        for address in addresses:
            if address.family == socket.AF_INET:
                ipv4 = address.address
            elif address.family == socket.AF_INET6:
                ipv6 = address.address.split("%")[0]
            elif address.family == psutil.AF_LINK:
                mac = address.address

        interface = stats.get(name)

        typer.echo()

        info("Интерфейс", name, typer.colors.BLUE)

        if interface:
            info(
                "Статус",
                "Подключён" if interface.isup else "Отключён",
                typer.colors.GREEN if interface.isup else typer.colors.RED,
            )

            if interface.speed > 0:
                info("Скорость", f"{interface.speed} Мбит/с")

        if ipv4:
            info("IPv4", ipv4, typer.colors.GREEN)

        if ipv6:
            info("IPv6", ipv6, typer.colors.CYAN)

        if mac:
            info("MAC", mac, typer.colors.MAGENTA)



if __name__ == "__main__":
    typer.run(main)