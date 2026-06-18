from sourceguide.config import load_config


def test_load_config_reads_environment_values():
    config = load_config(
        {
            "OPENAI_API_KEY": "key",
            "OPENAI_BASE_URL": "https://example.com/v1",
            "SOURCEGUIDE_MODEL": "model-x",
            "SOURCEGUIDE_LANGUAGE": "zh-CN",
            "SOURCEGUIDE_OUTPUT_DIR": "out",
            "SOURCEGUIDE_DEPTH": "deep",
            "SOURCEGUIDE_TIMEOUT": "12.5",
            "SOURCEGUIDE_DEBUG": "true",
        }
    )

    assert config.api_key == "key"
    assert config.base_url == "https://example.com/v1"
    assert config.model == "model-x"
    assert config.output_dir == "out"
    assert config.depth == "deep"
    assert config.timeout == 12.5
    assert config.debug is True


def test_load_config_uses_defaults():
    config = load_config({})

    assert config.api_key is None
    assert config.base_url == "https://api.openai.com/v1"
    assert config.model == "gpt-4.1-mini"
    assert config.language == "zh-CN"
    assert config.output_dir == "docs/sourceguide"
    assert config.depth == "normal"

