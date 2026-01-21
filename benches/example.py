import nexuslog as logging
import time

logging.basicConfig(level=logging.Level.Info)

class A:
    log = logging.getLogger("A")

class B:
    log = logging.getLogger("B")

def main():
    a = A()
    b = B()

    for i in range(1000):
        a.log.info(f"Message {i} from A")

    a.log.shutdown()
    b.log.shutdown()

if __name__ == "__main__":
    main()
