import util.analyze as analyze
import util.notice as notice
import vars.general as general
import vars.stock as s

def main():
    # """ 単一銘柄で全テクニカル分析を実施 """
    # analyze.all_analyze_for_only_symbol(s.symbol)

    # """ 複数銘柄で全テクニカル分析を実施 """
    # analyze.all_analyze_for_multi_symbols(s.symbols)

    """ 複数銘柄で特定のテクニカル分析を実施 """
    analyze.to_be_analyze(s.symbols)

    # """ LINE Notify API で分析結果をLINEに通知 """
    # if general.http_status_success == notice.check_line_notify_request(general.request_headers):
    #     notice.send_line_notify(general.request_headers, general.send_message, general.file_list)

if __name__ == '__main__':
    main()