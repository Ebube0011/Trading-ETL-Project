from Serve.Analytics import serve_analytics
from Serve.Reverse_etl import serve_reverse_etl


def main():
    serve_analytics()
    serve_reverse_etl()


if __name__ == "__main__":
    main()