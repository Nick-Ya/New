#include <iostream>
#include <thread>
#include <atomic>
#include <vector>
#include <csignal>
#include <cstdint>
#include <cstddef>
#include <array>

#include <boost/asio.hpp>
#include <grpcpp/grpcpp.h>

#include "monitor.grpc.pb.h"

using grpc::ServerContext;
using grpc::Status;
using monitor::Empty;
using monitor::BoolResponse;
using monitor::UdpStats;
using monitor::MonitorService;

// ================== gRPC SERVICE ==================
class MonitorServiceImpl final : public MonitorService::Service {
public:
    MonitorServiceImpl(std::atomic<bool>& ready,
                       std::atomic<uint32_t>& pkts,
                       std::atomic<uint32_t>& aBytes)
        : ready_(ready), pkts_(pkts), aBytes_(aBytes) {}

    Status IsReady(ServerContext*, const Empty*, BoolResponse* response) override {
        response->set_is_ready(ready_.load());
        return Status::OK;
    }

    Status GetUdpStatistics(ServerContext*, const Empty*, UdpStats* response) override {
        response->set_packets(pkts_.load());
        response->set_abytes(aBytes_.load());
        return Status::OK;
    }

private:
    std::atomic<bool>& ready_;
    std::atomic<uint32_t>& pkts_;
    std::atomic<uint32_t>& aBytes_;
};

// ================== UDP LISTENER ==================
class UdpListener {
public:
    UdpListener(boost::asio::io_context& io,
                uint16_t port,
                std::atomic<uint32_t>& pkts,
                std::atomic<uint32_t>& aBytes,
                std::atomic<bool>& running)
        : socket_(io, boost::asio::ip::udp::endpoint(
              boost::asio::ip::udp::v4(), port)),
          pkts_(pkts),
          aBytes_(aBytes),
          running_(running) {

        do_receive();
    }

    ~UdpListener() {
        close();
    }

    void close() {
        running_.store(false);
        boost::system::error_code ec;
        socket_.cancel(ec);
        socket_.close(ec);
    }

private:
    void do_receive() {
        socket_.async_receive_from(
            boost::asio::buffer(buffer_),
            remote_endpoint_,
            [this](boost::system::error_code ec, std::size_t bytes) {
                
                if (!running_.load()) {
                    return;
                }
                
                // Обработка ошибок и пустых пакетов
                if (ec) {
                    if (ec == boost::asio::error::operation_aborted) {
                        return;  // Операция отменена
                    }
                    // Для других ошибок продолжаем слушать
                    do_receive();
                    return;
                }
                
                // Игнорируем пустые пакеты
                if (bytes == 0) {
                    do_receive();
                    return;
                }
                
                // Увеличиваем счётчик только для валидных пакетов
                pkts_.fetch_add(1);
                
                // Подсчитываем количество букв 'A'
                uint32_t count_a = 0;
                for (std::size_t i = 0; i < bytes; ++i) {
                    if (buffer_[i] == 'A') {
                        count_a++;
                    }
                }
                
                if (count_a > 0) {
                    aBytes_.fetch_add(count_a);
                }
                
                // Продолжаем слушать
                do_receive();
            }
        );
    }

private:
    boost::asio::ip::udp::socket socket_;
    boost::asio::ip::udp::endpoint remote_endpoint_;
    std::array<char, 1500> buffer_{};

    std::atomic<uint32_t>& pkts_;
    std::atomic<uint32_t>& aBytes_;
    std::atomic<bool>& running_;
};

// ================== MAIN ==================
int main() {
    try {
        std::atomic<bool> is_ready{false};
        std::atomic<uint32_t> packet_count{0};
        std::atomic<uint32_t> a_bytes_count{0};
        std::atomic<bool> running{true};

        boost::asio::io_context io_ctx;

        MonitorServiceImpl service(is_ready, packet_count, a_bytes_count);

        grpc::ServerBuilder builder;
        builder.AddListeningPort("0.0.0.0:2031", grpc::InsecureServerCredentials());
        builder.RegisterService(&service);

        std::unique_ptr<grpc::Server> server = builder.BuildAndStart();

        std::cout << "[INFO] gRPC server started on 0.0.0.0:2031\n";

        UdpListener udp_listener(io_ctx, 2032, packet_count, a_bytes_count, running);

        is_ready.store(true);

        std::cout << "[INFO] UDP port opened on 0.0.0.0:2032. System is ready.\n";

        // Настройка обработки сигналов
        boost::asio::signal_set signals(io_ctx, SIGINT, SIGTERM);
        signals.async_wait([&](const boost::system::error_code& ec, int signal) {
            if (!ec) {
                std::cout << "\n[INFO] Shutdown signal (" << signal << ") received...\n";
                udp_listener.close();
                server->Shutdown();
                io_ctx.stop();
            }
        });

        std::thread io_thread([&]() {
            io_ctx.run();
        });

        server->Wait();
        io_thread.join();

        std::cout << "[INFO] Application terminated with exit code 0.\n";
        return 0;

    } catch (const std::exception& e) {
        std::cerr << "[FATAL] " << e.what() << "\n";
        return 1;
    }
}