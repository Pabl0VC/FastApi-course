from logscolor.logscl import infoL, traceL
import asyncio

async def tarea_lenta(tarea_id):
    infoL(f"Tarea {tarea_id}: empezando...")
    await asyncio.sleep(10)  # No bloquea
    traceL(f"Tarea {tarea_id}: terminada.")

async def main():
    await asyncio.gather(
        tarea_lenta(1),
        tarea_lenta(2),
    )

asyncio.run(main())

