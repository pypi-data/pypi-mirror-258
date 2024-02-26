import gradio as gr
import tensorflow as tf
import tensorflow_text

model = tf.saved_model.load('E:/sharaborno/saved_models/seq2seq_attn_translator')

inputs = [
    'mande skako man rana changgipa',
    # "well mannered"

    'na.a iako sa masina gita nanggen,je dakgualaniko na.a dakaha uko changgipino dakjana gita',
    # "you just have to understand that,the mistake you made should not be repeated again"

    'baju,anga shopping kamitingo banga choligija bosturangko raaha uani gimin anga skimenga'
    # "man,i have bought a lot of useless things while i'm shopping that's why i'm regretting"
]


def translate(src_seq, src_lang, tar_lang):
    return model.translate(tf.constant([src_seq]))[0].numpy().decode()


if __name__ == "__main__":
    iface = gr.Interface(
        fn=translate,
        inputs=[
            gr.Textbox(label="Input Text", placeholder="Input Text To Be Translated"),
            gr.Dropdown(label="From", choices=['en', 'bn', 'gr'], value="Garo"),
            gr.Dropdown(label="To", choices=['en', 'bn', 'gr'], value="Bangla")],
        outputs=gr.Textbox(label="Translation"), title="Translator", description="A machine translator.")

    iface.launch()
