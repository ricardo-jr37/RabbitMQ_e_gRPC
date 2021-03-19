# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import portao_pb2 as portao__pb2


class PortaoStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.abrirPortao = channel.unary_unary(
                '/Portao/abrirPortao',
                request_serializer=portao__pb2.StatusPortao.SerializeToString,
                response_deserializer=portao__pb2.StatusPortao.FromString,
                )
        self.fecharPortao = channel.unary_unary(
                '/Portao/fecharPortao',
                request_serializer=portao__pb2.StatusPortao.SerializeToString,
                response_deserializer=portao__pb2.StatusPortao.FromString,
                )


class PortaoServicer(object):
    """Missing associated documentation comment in .proto file."""

    def abrirPortao(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def fecharPortao(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PortaoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'abrirPortao': grpc.unary_unary_rpc_method_handler(
                    servicer.abrirPortao,
                    request_deserializer=portao__pb2.StatusPortao.FromString,
                    response_serializer=portao__pb2.StatusPortao.SerializeToString,
            ),
            'fecharPortao': grpc.unary_unary_rpc_method_handler(
                    servicer.fecharPortao,
                    request_deserializer=portao__pb2.StatusPortao.FromString,
                    response_serializer=portao__pb2.StatusPortao.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Portao', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Portao(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def abrirPortao(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Portao/abrirPortao',
            portao__pb2.StatusPortao.SerializeToString,
            portao__pb2.StatusPortao.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def fecharPortao(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Portao/fecharPortao',
            portao__pb2.StatusPortao.SerializeToString,
            portao__pb2.StatusPortao.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)