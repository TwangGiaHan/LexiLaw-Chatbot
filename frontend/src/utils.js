import { EventSourceParserStream } from 'eventsource-parser/stream';

export async function* parseSSEStream(stream) {
  const sseReader = stream
    .pipeThrough(new TextDecoderStream())
    .pipeThrough(new EventSourceParserStream())
    .getReader();
  
  while (true) {
    const { done, value } = await sseReader.read();
    if (done) break;
    // Bỏ qua data rỗng để tránh lỗi
    if (value.data && value.data.trim()) {
      yield value.data;
    }
  }
}