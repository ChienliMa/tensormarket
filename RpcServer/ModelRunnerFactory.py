import tensorflow as tf

class ModelRunner:
    def __init__(self, session, input_tensors, output_tensors):
        """
        input_tensors - dict{input_label, input_tensor}
        output_tensors - dict{output_label, output_tensor}
        """
        self.sess = session
        self.input_tensors = input_tensors
        self.output_tensors = output_tensors

    def run(self, input_datas):
        """
        inputs -> {input_label: input_data}
        """
        feed_dict = {}
        for input_label, input_tensor in self.input_tensors.iteritems():
            feed_dict[input_tensor] = input_datas[input_label]
        return self.sess.run(self.output_tensors, feed_dict)

    def stop(self):
        self.sess.close()

class ModelRunnerFactory:
    def __init__(self):
        pass

    def getRunner(self, model_dir, model_name, signature_key, input_labels, output_labels):
        sess = tf.Session()
     
        meta_graph_def = tf.saved_model.loader.load(sess, [model_name], model_dir)
        signature = meta_graph_def.signature_def

        input_tensor_names = map(lambda input_label: signature[signature_key].inputs[input_label].name, input_labels)
        output_tensor_names = map(lambda output_label: signature[signature_key].outputs[output_label].name, output_labels)

        input_tensors = map(lambda name: sess.graph.get_tensor_by_name(name), input_tensor_names)
        output_tensors = map(lambda name: sess.graph.get_tensor_by_name(name), output_tensor_names)

        input_tensors = dict([(input_label, input_tensor) for input_label, input_tensor in zip(input_labels, input_tensors)])
        output_tensors = dict([(output_label, output_tensor) for output_label, output_tensor in zip(output_labels, output_tensors)])
        return ModelRunner(sess, input_tensors, output_tensors)

def testModelRunner():
    model_dir = "../models/lol/logistic_mnist_graph"
    model_name  = "logistic_mnist_graph"
    signature_key = "main_signature"
    input_labels = ["input"]
    output_labels = ["output"]
    runner = ModelRunnerFactory().getRunner(model_dir, model_name, signature_key, input_labels, output_labels)

    test_data = {"input": [[0] * 784 ]}
    rval = runner.run(test_data)
    print rval
    assert output_labels == rval.keys()

if __name__ == "__main__":
    testModelRunner()