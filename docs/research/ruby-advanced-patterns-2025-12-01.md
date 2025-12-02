# Advanced Ruby Patterns: Comprehensive Guide
**Research Date:** 2025-12-01
**Focus:** Moderate to Difficult Use Cases
**Scope:** Ruby 3.x, Rails 7.x+, Best Practices

---

## Table of Contents
1. [Metaprogramming Patterns](#metaprogramming-patterns)
2. [Service Objects & Architecture](#service-objects--architecture)
3. [Rails Advanced Patterns](#rails-advanced-patterns)
4. [Testing Excellence](#testing-excellence)
5. [Concurrent Programming](#concurrent-programming)

---

## 1. Metaprogramming Patterns

### 1.1 Method Missing with Defensive Programming
**Difficulty:** Moderate
**When to Apply:** Creating DSLs, proxy objects, or dynamic method delegation

```ruby
# GOOD: Defensive method_missing with respond_to_missing?
class SmartProxy
  def initialize(target)
    @target = target
    @method_cache = {}
  end

  def method_missing(method_name, *args, &block)
    if @target.respond_to?(method_name)
      # Cache the method for performance
      define_singleton_method(method_name) do |*inner_args, &inner_block|
        log_method_call(method_name)
        @target.public_send(method_name, *inner_args, &inner_block)
      end

      public_send(method_name, *args, &block)
    else
      super
    end
  end

  def respond_to_missing?(method_name, include_private = false)
    @target.respond_to?(method_name, include_private) || super
  end

  private

  def log_method_call(method_name)
    puts "[PROXY] Called: #{method_name} at #{Time.now}"
  end
end

# Usage
user = User.new(name: "Alice")
proxy = SmartProxy.new(user)
proxy.name # Works and logs
proxy.respond_to?(:name) # => true (correct behavior)
```

**Performance Implications:**
- `method_missing` is slower than regular method dispatch
- Cache dynamically defined methods using `define_singleton_method`
- Always implement `respond_to_missing?` for correct introspection

**Testing Strategy:**
```ruby
RSpec.describe SmartProxy do
  let(:target) { double("Target", name: "Alice", age: 30) }
  let(:proxy) { SmartProxy.new(target) }

  describe "#method_missing" do
    it "delegates to target" do
      expect(proxy.name).to eq("Alice")
    end

    it "raises NoMethodError for undefined methods" do
      expect { proxy.undefined_method }.to raise_error(NoMethodError)
    end

    it "caches delegated methods" do
      proxy.name
      expect(proxy.singleton_methods).to include(:name)
    end
  end

  describe "#respond_to_missing?" do
    it "returns true for target methods" do
      expect(proxy).to respond_to(:name)
    end

    it "returns false for undefined methods" do
      expect(proxy).not_to respond_to(:undefined)
    end
  end
end
```

---

### 1.2 Module Composition with Refinements
**Difficulty:** Difficult
**When to Apply:** Adding scoped behavior without monkey-patching

```ruby
# Define refinement for scoped String extensions
module StringRefinements
  refine String do
    def titleize_advanced
      split(/[\s_-]/)
        .map { |word| word.capitalize }
        .join(' ')
        .gsub(/\b(Of|And|The|In|On|At)\b/i) { |match| match.downcase }
        .sub(/\A\w/) { |char| char.upcase }
    end

    def to_slug
      downcase
        .gsub(/[^a-z0-9\s-]/, '')
        .gsub(/\s+/, '-')
        .squeeze('-')
    end
  end
end

# Use refinements in specific scope
class Article
  using StringRefinements

  attr_reader :title, :slug

  def initialize(title)
    @title = title.titleize_advanced
    @slug = title.to_slug
  end
end

# Refinements are scoped - doesn't affect global String
article = Article.new("the-lord_of the rings")
article.title # => "The Lord of the Rings"
article.slug  # => "the-lord-of-the-rings"

# Outside the class, String doesn't have these methods
"test".respond_to?(:to_slug) # => false
```

**Performance Implications:**
- Refinements have minimal performance overhead
- Safer than monkey-patching (no global state pollution)
- Method lookup slightly slower than monkey-patches

**Rails Integration:**
```ruby
# app/refinements/active_record_refinements.rb
module ActiveRecordRefinements
  refine ActiveRecord::Relation do
    def with_includes(*associations)
      includes(*associations).references(*associations)
    end

    def by_recent(limit = 10)
      order(created_at: :desc).limit(limit)
    end
  end
end

# app/queries/user_query.rb
class UserQuery
  using ActiveRecordRefinements

  def self.recent_active_users
    User.active
        .with_includes(:posts, :comments)
        .by_recent(20)
  end
end
```

---

### 1.3 Class Macros and DSL Building
**Difficulty:** Difficult
**When to Apply:** Creating framework-like features, configuration DSLs

```ruby
# Advanced class macro system with validation
module Validatable
  def self.included(base)
    base.extend(ClassMethods)
  end

  module ClassMethods
    def validates(field, **rules)
      @validations ||= {}
      @validations[field] = rules

      # Define getter/setter with validation
      define_method(field) do
        instance_variable_get("@#{field}")
      end

      define_method("#{field}=") do |value|
        self.class.validate_field!(field, value)
        instance_variable_set("@#{field}", value)
      end
    end

    def validate_field!(field, value)
      rules = @validations[field] || {}

      if rules[:presence] && value.nil?
        raise ValidationError, "#{field} cannot be nil"
      end

      if rules[:type] && !value.is_a?(rules[:type])
        raise ValidationError, "#{field} must be a #{rules[:type]}"
      end

      if rules[:format] && value !~ rules[:format]
        raise ValidationError, "#{field} format is invalid"
      end

      if rules[:custom]&.respond_to?(:call)
        rules[:custom].call(value) or raise ValidationError, "#{field} failed custom validation"
      end
    end

    def validations
      @validations ||= {}
    end
  end

  class ValidationError < StandardError; end
end

# Usage: Create a validated user class
class User
  include Validatable

  validates :email,
    presence: true,
    type: String,
    format: /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i

  validates :age,
    type: Integer,
    custom: ->(val) { val >= 18 }

  validates :name,
    presence: true,
    type: String

  def initialize(email:, age:, name:)
    self.email = email
    self.age = age
    self.name = name
  end
end

# Testing
user = User.new(email: "alice@example.com", age: 25, name: "Alice")
user.email = "invalid" # Raises ValidationError
user.age = 15          # Raises ValidationError
```

**Performance Implications:**
- Macros execute at class definition time (minimal runtime cost)
- Dynamic method definition faster than `method_missing`
- Validation overhead on each setter call

**Testing Strategy:**
```ruby
RSpec.describe Validatable do
  let(:user_class) do
    Class.new do
      include Validatable
      validates :email, presence: true, format: /@/
      validates :age, type: Integer
    end
  end

  describe ".validates" do
    it "creates getter and setter methods" do
      instance = user_class.new
      expect(instance).to respond_to(:email)
      expect(instance).to respond_to(:email=)
    end

    it "validates presence" do
      instance = user_class.new
      expect { instance.email = nil }.to raise_error(Validatable::ValidationError)
    end

    it "validates format" do
      instance = user_class.new
      expect { instance.email = "invalid" }.to raise_error(Validatable::ValidationError)
    end

    it "validates type" do
      instance = user_class.new
      expect { instance.age = "twenty" }.to raise_error(Validatable::ValidationError)
    end
  end
end
```

---

### 1.4 Eigenclass Patterns for Singleton Behavior
**Difficulty:** Difficult
**When to Apply:** Per-object behavior, singleton methods, class-level DSLs

```ruby
# Advanced eigenclass manipulation
module Configurable
  def configure(&block)
    eigenclass = class << self; self; end
    eigenclass.class_eval(&block)
  end

  def config
    @config ||= {}
  end
end

class APIClient
  extend Configurable

  configure do
    def endpoint(name, path:, method: :get)
      config[name] = { path: path, method: method }

      define_singleton_method(name) do |**params|
        request(config[name][:method], config[name][:path], params)
      end
    end

    def base_url(url)
      config[:base_url] = url
    end
  end

  def self.request(method, path, params)
    uri = URI.join(config[:base_url], path)
    # HTTP request logic here
    { method: method, uri: uri, params: params }
  end
end

# Usage: Define API endpoints via DSL
APIClient.configure do
  base_url "https://api.example.com"
  endpoint :list_users, path: "/users"
  endpoint :create_user, path: "/users", method: :post
  endpoint :get_user, path: "/users/:id"
end

# Call defined endpoints
APIClient.list_users(limit: 10)
APIClient.create_user(name: "Alice", email: "alice@example.com")
```

**Per-Object Eigenclass Patterns:**
```ruby
# Add methods to specific instances
class Document
  attr_accessor :content
end

doc = Document.new
doc.content = "Sample"

# Add singleton method to this specific instance
class << doc
  def render_markdown
    # Markdown rendering logic
    content.gsub(/\*\*(.+?)\*\*/, '<strong>\1</strong>')
  end

  def word_count
    content.split.size
  end
end

doc.render_markdown # Works
other_doc = Document.new
other_doc.respond_to?(:render_markdown) # => false
```

**Performance Implications:**
- Eigenclass creation is fast (Ruby optimizes this)
- Singleton methods stored in object's eigenclass
- No performance penalty for method lookup

---

## 2. Service Objects & Architecture

### 2.1 PORO Service Objects with Dependency Injection
**Difficulty:** Moderate
**When to Apply:** Complex business logic, multi-step operations, testability

```ruby
# Service object with constructor injection
class UserRegistrationService
  Result = Struct.new(:success?, :user, :errors, keyword_init: true) do
    def failure?
      !success?
    end
  end

  def initialize(
    user_repository: UserRepository.new,
    email_service: EmailService.new,
    analytics: Analytics.new
  )
    @user_repository = user_repository
    @email_service = email_service
    @analytics = analytics
  end

  def call(params)
    user = build_user(params)

    return failure_result(user.errors) unless user.valid?

    begin
      saved_user = @user_repository.save(user)
      send_welcome_email(saved_user)
      track_registration(saved_user)

      success_result(saved_user)
    rescue StandardError => e
      failure_result(["Registration failed: #{e.message}"])
    end
  end

  private

  def build_user(params)
    User.new(
      email: params[:email],
      name: params[:name],
      password: params[:password]
    )
  end

  def send_welcome_email(user)
    @email_service.send_welcome(user.email, user.name)
  end

  def track_registration(user)
    @analytics.track('user_registered', user_id: user.id)
  end

  def success_result(user)
    Result.new(success?: true, user: user, errors: [])
  end

  def failure_result(errors)
    Result.new(success?: false, user: nil, errors: errors)
  end
end

# Usage
service = UserRegistrationService.new
result = service.call(email: "alice@example.com", name: "Alice", password: "secret")

if result.success?
  puts "Welcome, #{result.user.name}!"
else
  puts "Errors: #{result.errors.join(', ')}"
end
```

**Rails Integration:**
```ruby
# app/services/user_registration_service.rb
class UserRegistrationService < ApplicationService
  def initialize(user_repository: User, **deps)
    super(**deps)
    @user_repository = user_repository
  end

  # ... rest of implementation
end

# app/controllers/users_controller.rb
class UsersController < ApplicationController
  def create
    result = UserRegistrationService.new.call(user_params)

    if result.success?
      session[:user_id] = result.user.id
      redirect_to dashboard_path, notice: "Welcome!"
    else
      @errors = result.errors
      render :new, status: :unprocessable_entity
    end
  end

  private

  def user_params
    params.require(:user).permit(:email, :name, :password)
  end
end
```

**Testing Strategy:**
```ruby
RSpec.describe UserRegistrationService do
  let(:user_repository) { instance_double(UserRepository) }
  let(:email_service) { instance_double(EmailService) }
  let(:analytics) { instance_double(Analytics) }

  let(:service) do
    described_class.new(
      user_repository: user_repository,
      email_service: email_service,
      analytics: analytics
    )
  end

  describe "#call" do
    let(:params) { { email: "alice@example.com", name: "Alice", password: "secret" } }

    context "when successful" do
      let(:user) { instance_double(User, id: 1, valid?: true, errors: []) }

      before do
        allow(User).to receive(:new).and_return(user)
        allow(user_repository).to receive(:save).and_return(user)
        allow(email_service).to receive(:send_welcome)
        allow(analytics).to receive(:track)
      end

      it "returns success result" do
        result = service.call(params)
        expect(result).to be_success
        expect(result.user).to eq(user)
      end

      it "sends welcome email" do
        service.call(params)
        expect(email_service).to have_received(:send_welcome).with("alice@example.com", "Alice")
      end

      it "tracks registration" do
        service.call(params)
        expect(analytics).to have_received(:track).with('user_registered', user_id: 1)
      end
    end

    context "when user is invalid" do
      let(:user) { instance_double(User, valid?: false, errors: ["Email is invalid"]) }

      before do
        allow(User).to receive(:new).and_return(user)
      end

      it "returns failure result" do
        result = service.call(params)
        expect(result).to be_failure
        expect(result.errors).to include("Email is invalid")
      end

      it "does not save user" do
        service.call(params)
        expect(user_repository).not_to have_received(:save)
      end
    end
  end
end
```

---

### 2.2 Interactor Pattern with Rollback Support
**Difficulty:** Difficult
**When to Apply:** Multi-step transactions, complex workflows requiring rollback

```ruby
# Base interactor with rollback support
class Interactor
  class Failure < StandardError; end

  attr_reader :context

  def self.call(**args)
    new(**args).tap(&:run)
  end

  def initialize(**args)
    @context = OpenStruct.new(args)
    @context.success = true
    @rollback_stack = []
  end

  def run
    call
  rescue Failure => e
    @context.success = false
    @context.error = e.message
    rollback
  end

  def call
    raise NotImplementedError
  end

  def rollback
    @rollback_stack.reverse_each(&:call)
  end

  def fail!(message)
    raise Failure, message
  end

  def on_rollback(&block)
    @rollback_stack << block
  end

  def success?
    @context.success
  end

  def failure?
    !success?
  end
end

# Organizer for chaining interactors
class Organizer < Interactor
  def self.organize(*interactors)
    @interactors = interactors
  end

  def self.interactors
    @interactors || []
  end

  def call
    self.class.interactors.each do |interactor_class|
      result = interactor_class.call(**@context.to_h)

      if result.failure?
        @context = result.context
        fail!(@context.error)
      end

      @context = result.context
    end
  end
end

# Example: Order processing workflow
class CreateOrder < Interactor
  def call
    order = Order.create!(
      user_id: context.user_id,
      items: context.items
    )

    context.order = order

    on_rollback do
      order.destroy
    end
  end
end

class ChargePayment < Interactor
  def call
    charge = PaymentGateway.charge(
      amount: context.order.total,
      token: context.payment_token
    )

    fail!("Payment failed: #{charge.error}") unless charge.success?

    context.charge = charge

    on_rollback do
      PaymentGateway.refund(charge.id)
    end
  end
end

class SendConfirmation < Interactor
  def call
    Mailer.order_confirmation(context.order).deliver_now

    on_rollback do
      # Send cancellation email
      Mailer.order_cancelled(context.order).deliver_now
    end
  end
end

class ProcessOrder < Organizer
  organize CreateOrder, ChargePayment, SendConfirmation
end

# Usage
result = ProcessOrder.call(
  user_id: 1,
  items: [{ product_id: 1, quantity: 2 }],
  payment_token: "tok_abc123"
)

if result.success?
  puts "Order #{result.context.order.id} processed successfully"
else
  puts "Order failed: #{result.context.error}"
  # All previous steps have been rolled back automatically
end
```

**Performance Implications:**
- Each interactor creates OpenStruct (lightweight)
- Rollback stack grows linearly with steps
- Network I/O in rollback can be slow (design for idempotency)

**Testing Strategy:**
```ruby
RSpec.describe ProcessOrder do
  let(:user_id) { 1 }
  let(:items) { [{ product_id: 1, quantity: 2 }] }
  let(:payment_token) { "tok_test" }

  describe ".call" do
    context "when all steps succeed" do
      before do
        allow(Order).to receive(:create!).and_return(double(id: 1, total: 100))
        allow(PaymentGateway).to receive(:charge).and_return(double(success?: true, id: "ch_123"))
        allow(Mailer).to receive_message_chain(:order_confirmation, :deliver_now)
      end

      it "creates order" do
        ProcessOrder.call(user_id: user_id, items: items, payment_token: payment_token)
        expect(Order).to have_received(:create!)
      end

      it "charges payment" do
        ProcessOrder.call(user_id: user_id, items: items, payment_token: payment_token)
        expect(PaymentGateway).to have_received(:charge)
      end

      it "sends confirmation" do
        ProcessOrder.call(user_id: user_id, items: items, payment_token: payment_token)
        expect(Mailer).to have_received(:order_confirmation)
      end
    end

    context "when payment fails" do
      let(:order) { double(id: 1, total: 100, destroy: true) }

      before do
        allow(Order).to receive(:create!).and_return(order)
        allow(PaymentGateway).to receive(:charge).and_return(double(success?: false, error: "Card declined"))
      end

      it "rolls back order creation" do
        ProcessOrder.call(user_id: user_id, items: items, payment_token: payment_token)
        expect(order).to have_received(:destroy)
      end

      it "returns failure" do
        result = ProcessOrder.call(user_id: user_id, items: items, payment_token: payment_token)
        expect(result).to be_failure
        expect(result.context.error).to include("Payment failed")
      end
    end
  end
end
```

---

### 2.3 Query Objects for Complex ActiveRecord Queries
**Difficulty:** Moderate
**When to Apply:** Complex queries, reusable filters, performance optimization

```ruby
# Base query object
class ApplicationQuery
  def initialize(relation = default_relation)
    @relation = relation
  end

  def call
    @relation
  end

  private

  def default_relation
    raise NotImplementedError
  end
end

# Advanced query with chainable scopes
class UserQuery < ApplicationQuery
  def active
    @relation = @relation.where(status: 'active')
    self
  end

  def with_role(role)
    @relation = @relation.where(role: role)
    self
  end

  def created_after(date)
    @relation = @relation.where('created_at > ?', date)
    self
  end

  def with_recent_activity(days = 30)
    @relation = @relation
      .joins(:activities)
      .where('activities.created_at > ?', days.days.ago)
      .distinct
    self
  end

  def search(term)
    @relation = @relation.where(
      'name ILIKE :term OR email ILIKE :term',
      term: "%#{term}%"
    )
    self
  end

  def with_stats
    @relation = @relation.select(
      'users.*',
      '(SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) as posts_count',
      '(SELECT COUNT(*) FROM comments WHERE comments.user_id = users.id) as comments_count'
    )
    self
  end

  def ordered(direction = :desc)
    @relation = @relation.order(created_at: direction)
    self
  end

  def paginate(page: 1, per_page: 20)
    offset = (page - 1) * per_page
    @relation = @relation.limit(per_page).offset(offset)
    self
  end

  private

  def default_relation
    User.all
  end
end

# Usage: Chainable and composable
recent_admins = UserQuery.new
  .active
  .with_role('admin')
  .with_recent_activity(7)
  .with_stats
  .ordered(:desc)
  .paginate(page: 1, per_page: 10)
  .call

# Alternative: Named query classes
class ActiveAdminsQuery < ApplicationQuery
  def initialize(relation = User.all, activity_days: 30)
    super(relation)
    @activity_days = activity_days
  end

  def call
    @relation
      .where(status: 'active', role: 'admin')
      .joins(:activities)
      .where('activities.created_at > ?', @activity_days.days.ago)
      .distinct
      .select('users.*', 'MAX(activities.created_at) as last_activity_at')
      .group('users.id')
      .order('last_activity_at DESC')
  end

  private

  def default_relation
    User.all
  end
end

# Usage
admins = ActiveAdminsQuery.new(activity_days: 7).call
```

**Rails Integration:**
```ruby
# app/queries/user_query.rb
class UserQuery < ApplicationQuery
  # ... implementation
end

# app/controllers/admin/users_controller.rb
class Admin::UsersController < Admin::BaseController
  def index
    @users = UserQuery.new
      .active
      .with_role(params[:role]) if params[:role].present?
      .search(params[:q]) if params[:q].present?
      .ordered(:desc)
      .paginate(page: params[:page], per_page: 20)
      .call
  end
end
```

**Performance Implications:**
- Query objects prevent N+1 queries via strategic `joins`/`includes`
- Chainable design allows query optimization before execution
- Use `select` to limit columns, reducing memory usage
- Consider database indexes for frequent query patterns

**Testing Strategy:**
```ruby
RSpec.describe UserQuery do
  describe "#active" do
    let!(:active_user) { create(:user, status: 'active') }
    let!(:inactive_user) { create(:user, status: 'inactive') }

    it "returns only active users" do
      result = described_class.new.active.call
      expect(result).to include(active_user)
      expect(result).not_to include(inactive_user)
    end
  end

  describe "#with_stats" do
    let!(:user) { create(:user) }
    let!(:posts) { create_list(:post, 3, user: user) }

    it "includes post count" do
      result = described_class.new.with_stats.call.first
      expect(result.posts_count).to eq(3)
    end
  end

  describe "chaining" do
    let!(:admin) { create(:user, role: 'admin', status: 'active') }
    let!(:user) { create(:user, role: 'user', status: 'active') }

    it "chains filters correctly" do
      result = described_class.new.active.with_role('admin').call
      expect(result).to eq([admin])
    end
  end
end
```

---

### 2.4 Form Objects for Complex Forms
**Difficulty:** Moderate
**When to Apply:** Multi-model forms, complex validations, form-specific logic

```ruby
# Form object with nested attributes
class UserProfileForm
  include ActiveModel::Model
  include ActiveModel::Validations

  attr_accessor :user_id, :name, :email, :bio,
                :address_street, :address_city, :address_zip,
                :preferences

  validates :name, presence: true, length: { minimum: 2 }
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :address_city, presence: true
  validate :validate_preferences

  def initialize(attributes = {})
    @preferences = {}
    super(attributes)
  end

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      update_user
      update_address
      update_preferences
    end

    true
  rescue ActiveRecord::RecordInvalid
    false
  end

  def persisted?
    user_id.present?
  end

  private

  def user
    @user ||= User.find(user_id) if user_id.present?
  end

  def update_user
    if user
      user.update!(name: name, email: email, bio: bio)
    else
      @user = User.create!(name: name, email: email, bio: bio)
      self.user_id = @user.id
    end
  end

  def update_address
    address = user.address || user.build_address
    address.update!(
      street: address_street,
      city: address_city,
      zip: address_zip
    )
  end

  def update_preferences
    user.preferences.update!(preferences)
  end

  def validate_preferences
    required_keys = %w[theme language timezone]
    missing = required_keys - preferences.keys.map(&:to_s)

    errors.add(:preferences, "missing required keys: #{missing.join(', ')}") if missing.any?
  end
end

# Usage in controller
class ProfilesController < ApplicationController
  def update
    @form = UserProfileForm.new(form_params.merge(user_id: current_user.id))

    if @form.save
      redirect_to profile_path, notice: "Profile updated successfully"
    else
      render :edit, status: :unprocessable_entity
    end
  end

  private

  def form_params
    params.require(:user_profile_form).permit(
      :name, :email, :bio,
      :address_street, :address_city, :address_zip,
      preferences: [:theme, :language, :timezone]
    )
  end
end
```

**Advanced: Multi-Step Form Object**
```ruby
class MultiStepFormBase
  include ActiveModel::Model

  attr_accessor :current_step

  STEPS = [].freeze

  def initialize(attributes = {})
    @current_step = attributes[:current_step]&.to_sym || self.class::STEPS.first
    super(attributes)
  end

  def valid?(step = current_step)
    super() && validations_for_step(step)
  end

  def next_step
    current_index = self.class::STEPS.index(current_step)
    self.class::STEPS[current_index + 1] if current_index
  end

  def previous_step
    current_index = self.class::STEPS.index(current_step)
    self.class::STEPS[current_index - 1] if current_index && current_index > 0
  end

  def last_step?
    current_step == self.class::STEPS.last
  end

  private

  def validations_for_step(step)
    # Override in subclass
    true
  end
end

class UserRegistrationForm < MultiStepFormBase
  STEPS = [:account, :profile, :preferences].freeze

  attr_accessor :email, :password, :password_confirmation,
                :name, :bio, :avatar,
                :theme, :language

  validates :email, presence: true, if: -> { current_step == :account }
  validates :password, presence: true, length: { minimum: 8 }, if: -> { current_step == :account }
  validates :password_confirmation, presence: true, if: -> { current_step == :account }
  validate :passwords_match, if: -> { current_step == :account }

  validates :name, presence: true, if: -> { current_step == :profile }

  validates :theme, inclusion: { in: %w[light dark] }, if: -> { current_step == :preferences }
  validates :language, inclusion: { in: %w[en es fr] }, if: -> { current_step == :preferences }

  def save
    return false unless valid?(current_step)
    return true unless last_step?

    persist_user
  end

  private

  def passwords_match
    errors.add(:password_confirmation, "doesn't match") if password != password_confirmation
  end

  def persist_user
    ActiveRecord::Base.transaction do
      user = User.create!(email: email, password: password, name: name, bio: bio)
      user.create_preferences!(theme: theme, language: language)
    end
    true
  rescue ActiveRecord::RecordInvalid
    false
  end
end
```

**Testing Strategy:**
```ruby
RSpec.describe UserProfileForm do
  describe "validations" do
    it "validates name presence" do
      form = UserProfileForm.new(name: "")
      expect(form).not_to be_valid
      expect(form.errors[:name]).to include("can't be blank")
    end

    it "validates email format" do
      form = UserProfileForm.new(email: "invalid")
      expect(form).not_to be_valid
      expect(form.errors[:email]).to include("is invalid")
    end
  end

  describe "#save" do
    let(:user) { create(:user) }
    let(:valid_attributes) do
      {
        user_id: user.id,
        name: "Alice",
        email: "alice@example.com",
        address_city: "New York",
        preferences: { theme: "dark", language: "en", timezone: "EST" }
      }
    end

    it "updates user attributes" do
      form = UserProfileForm.new(valid_attributes)
      expect { form.save }.to change { user.reload.name }.to("Alice")
    end

    it "updates nested address" do
      form = UserProfileForm.new(valid_attributes)
      form.save
      expect(user.reload.address.city).to eq("New York")
    end

    it "returns false when invalid" do
      form = UserProfileForm.new(user_id: user.id, name: "")
      expect(form.save).to be false
    end
  end
end
```

---

### 2.5 Repository Pattern for Data Access
**Difficulty:** Moderate
**When to Apply:** Abstracting data access, testing without database, multi-source data

```ruby
# Repository interface
class Repository
  def find(id)
    raise NotImplementedError
  end

  def find_by(conditions)
    raise NotImplementedError
  end

  def all
    raise NotImplementedError
  end

  def save(entity)
    raise NotImplementedError
  end

  def delete(id)
    raise NotImplementedError
  end
end

# ActiveRecord repository implementation
class ActiveRecordUserRepository < Repository
  def find(id)
    User.find(id)
  rescue ActiveRecord::RecordNotFound
    nil
  end

  def find_by(conditions)
    User.find_by(conditions)
  end

  def all
    User.all.to_a
  end

  def where(conditions)
    User.where(conditions).to_a
  end

  def save(user)
    if user.persisted?
      user.save
    else
      user.save
    end
    user
  end

  def delete(id)
    user = find(id)
    user&.destroy
  end

  def with_recent_posts(days = 7)
    User.joins(:posts)
        .where('posts.created_at > ?', days.days.ago)
        .distinct
        .to_a
  end
end

# In-memory repository for testing
class InMemoryUserRepository < Repository
  def initialize
    @users = {}
    @next_id = 1
  end

  def find(id)
    @users[id.to_i]
  end

  def find_by(conditions)
    @users.values.find do |user|
      conditions.all? { |key, value| user.public_send(key) == value }
    end
  end

  def all
    @users.values
  end

  def where(conditions)
    @users.values.select do |user|
      conditions.all? { |key, value| user.public_send(key) == value }
    end
  end

  def save(user)
    if user.id.nil?
      user.id = @next_id
      @next_id += 1
    end
    @users[user.id] = user
    user
  end

  def delete(id)
    @users.delete(id.to_i)
  end

  def clear
    @users.clear
    @next_id = 1
  end
end

# Usage with dependency injection
class UserService
  def initialize(repository: ActiveRecordUserRepository.new)
    @repository = repository
  end

  def find_active_user(id)
    user = @repository.find(id)
    user if user&.active?
  end

  def create_user(attributes)
    user = User.new(attributes)
    @repository.save(user) if user.valid?
  end
end

# Testing with in-memory repository
RSpec.describe UserService do
  let(:repository) { InMemoryUserRepository.new }
  let(:service) { UserService.new(repository: repository) }

  after { repository.clear }

  describe "#find_active_user" do
    it "returns active user" do
      user = User.new(id: 1, status: 'active', name: 'Alice')
      repository.save(user)

      expect(service.find_active_user(1)).to eq(user)
    end

    it "returns nil for inactive user" do
      user = User.new(id: 1, status: 'inactive', name: 'Bob')
      repository.save(user)

      expect(service.find_active_user(1)).to be_nil
    end
  end
end
```

**Performance Implications:**
- Repository pattern adds abstraction layer (minimal overhead)
- In-memory repositories fast for testing (no database I/O)
- Can implement caching at repository level

---

## 3. Rails Advanced Patterns

### 3.1 ActiveRecord Query Optimization
**Difficulty:** Moderate to Difficult
**When to Apply:** N+1 queries, slow queries, high-traffic endpoints

```ruby
# BAD: N+1 query problem
def show_users_with_posts
  User.all.each do |user|
    puts "#{user.name}: #{user.posts.count} posts" # N+1 query!
  end
end

# GOOD: Eager loading with includes
def show_users_with_posts_optimized
  User.includes(:posts).each do |user|
    puts "#{user.name}: #{user.posts.size} posts" # No additional queries
  end
end

# ADVANCED: Strategic eager loading based on usage
class User < ApplicationRecord
  has_many :posts
  has_many :comments

  # Define scopes for common eager loading patterns
  scope :with_content, -> { includes(:posts, :comments) }
  scope :with_posts_and_tags, -> { includes(posts: :tags) }

  # Use preload when you don't need WHERE conditions on associations
  scope :with_preloaded_posts, -> { preload(:posts) }

  # Use eager_load when you need WHERE on associations
  scope :with_recent_posts, -> {
    eager_load(:posts).where('posts.created_at > ?', 1.week.ago)
  }

  # Use joins for filtering without loading associations
  scope :having_posts, -> { joins(:posts).distinct }
end

# Counter cache for performance
class Post < ApplicationRecord
  belongs_to :user, counter_cache: true
end

class User < ApplicationRecord
  has_many :posts
  # Now user.posts.count becomes user.posts_count (no query)
end

# Advanced: Batch processing to avoid memory bloat
def process_all_users
  User.find_each(batch_size: 1000) do |user|
    # Process user
    # Automatically breaks into batches to prevent loading all records
  end
end

# Select only needed columns to reduce memory
def user_names_and_emails
  User.select(:id, :name, :email).map { |u| [u.name, u.email] }
end

# Pluck for even better performance (returns arrays, not AR objects)
def user_names_optimized
  User.pluck(:name) # Returns array of strings directly
end

# Complex optimization: Subqueries
class User < ApplicationRecord
  scope :with_post_count, -> {
    select('users.*, (SELECT COUNT(*) FROM posts WHERE posts.user_id = users.id) as posts_count')
  }
end

# Usage
users = User.with_post_count
users.first.posts_count # No additional query, value from subquery
```

**Performance Measurement:**
```ruby
# Use ActiveRecord query logging
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Or use benchmark
require 'benchmark'

time = Benchmark.measure do
  User.includes(:posts).to_a
end

puts "Time: #{time.real} seconds"

# Use Bullet gem to detect N+1 queries in development
# Gemfile
gem 'bullet', group: :development

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.console = true
end
```

**Testing for Performance:**
```ruby
RSpec.describe "User queries" do
  describe "N+1 prevention" do
    it "does not create N+1 queries" do
      create_list(:user, 3, :with_posts)

      expect {
        User.includes(:posts).each do |user|
          user.posts.to_a
        end
      }.to make_database_queries(count: 2) # 1 for users, 1 for posts
    end
  end
end
```

---

### 3.2 Background Jobs with Sidekiq Patterns
**Difficulty:** Moderate
**When to Apply:** Async processing, scheduled tasks, retry logic

```ruby
# Basic Sidekiq job
class EmailWorker
  include Sidekiq::Worker

  sidekiq_options retry: 3, queue: :mailers

  def perform(user_id, email_type)
    user = User.find(user_id)
    UserMailer.public_send(email_type, user).deliver_now
  end
end

# Usage
EmailWorker.perform_async(user.id, :welcome_email)

# Advanced: Job with custom retry logic
class PaymentProcessorWorker
  include Sidekiq::Worker

  sidekiq_options retry: 5, queue: :critical

  # Exponential backoff
  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGateway::NetworkError
      10 * (count + 1) # 10s, 20s, 30s, 40s, 50s
    when PaymentGateway::RateLimitError
      300 # 5 minutes
    else
      :kill # Don't retry other errors
    end
  end

  def perform(order_id, payment_token)
    order = Order.find(order_id)

    result = PaymentGateway.charge(
      amount: order.total,
      token: payment_token
    )

    if result.success?
      order.update!(status: 'paid', payment_id: result.id)
    else
      raise PaymentGateway::ChargeFailedError, result.error
    end
  end
end

# Pattern: Idempotent jobs
class UserActivationWorker
  include Sidekiq::Worker

  def perform(user_id)
    user = User.find(user_id)

    # Idempotent: safe to run multiple times
    return if user.activated?

    user.transaction do
      user.update!(activated: true, activated_at: Time.current)
      UserMailer.activation_confirmation(user).deliver_now
    end
  end
end

# Pattern: Batch processing
class BulkEmailWorker
  include Sidekiq::Worker

  def perform(campaign_id)
    campaign = Campaign.find(campaign_id)

    campaign.users.find_each(batch_size: 100) do |user|
      EmailWorker.perform_async(user.id, :campaign_email)
    end
  end
end

# Advanced: Unique jobs (requires sidekiq-unique-jobs gem)
class ReportGeneratorWorker
  include Sidekiq::Worker

  sidekiq_options lock: :until_executed,
                   on_conflict: :log

  def perform(user_id, report_type)
    user = User.find(user_id)
    report = ReportGenerator.new(user, report_type).generate

    UserMailer.report_ready(user, report).deliver_now
  end
end

# Pattern: Scheduled jobs
class DailyReportWorker
  include Sidekiq::Worker

  def perform
    User.where(receive_daily_report: true).find_each do |user|
      ReportGeneratorWorker.perform_async(user.id, :daily)
    end
  end
end

# Schedule in config/initializers/sidekiq.rb
# Using sidekiq-scheduler gem
Sidekiq.configure_server do |config|
  config.on(:startup) do
    Sidekiq.schedule = {
      'daily_report' => {
        'cron' => '0 6 * * *', # 6am daily
        'class' => 'DailyReportWorker'
      }
    }
  end
end
```

**Testing Sidekiq Jobs:**
```ruby
RSpec.describe EmailWorker do
  describe "#perform" do
    let(:user) { create(:user) }

    it "sends email" do
      expect {
        described_class.new.perform(user.id, :welcome_email)
      }.to change { ActionMailer::Base.deliveries.count }.by(1)
    end
  end

  describe "job enqueuing" do
    it "enqueues job" do
      expect {
        EmailWorker.perform_async(user.id, :welcome_email)
      }.to change(EmailWorker.jobs, :size).by(1)
    end
  end
end

# Test scheduled jobs
RSpec.describe DailyReportWorker do
  it "schedules report for eligible users" do
    user = create(:user, receive_daily_report: true)

    described_class.new.perform

    expect(ReportGeneratorWorker).to have_enqueued_sidekiq_job(user.id, :daily)
  end
end
```

---

### 3.3 Concerns and Decorators
**Difficulty:** Moderate
**When to Apply:** Shared behavior, presentation logic separation

```ruby
# ActiveSupport::Concern for shared model behavior
module Trackable
  extend ActiveSupport::Concern

  included do
    has_many :activities, as: :trackable, dependent: :destroy

    after_create :track_creation
    after_update :track_update
  end

  class_methods do
    def tracked_attributes(*attrs)
      @tracked_attributes = attrs
    end

    def get_tracked_attributes
      @tracked_attributes || []
    end
  end

  def track_event(event_type, metadata = {})
    activities.create!(
      event_type: event_type,
      metadata: metadata,
      user: Current.user
    )
  end

  private

  def track_creation
    track_event('created')
  end

  def track_update
    changes = saved_changes.slice(*self.class.get_tracked_attributes)
    track_event('updated', changes: changes) if changes.any?
  end
end

# Usage in models
class Post < ApplicationRecord
  include Trackable

  tracked_attributes :title, :status
end

class User < ApplicationRecord
  include Trackable

  tracked_attributes :name, :email
end

# Decorator pattern (using Draper or plain Ruby)
class UserDecorator < SimpleDelegator
  def full_name
    "#{first_name} #{last_name}"
  end

  def avatar_url(size: :medium)
    avatar.present? ? avatar.variant(resize_to_limit: sizes[size]) : default_avatar
  end

  def membership_badge
    return "👑 Premium" if premium?
    return "⭐ Pro" if pro?
    "🆓 Free"
  end

  def formatted_created_at
    created_at.strftime("%B %d, %Y")
  end

  private

  def sizes
    { small: [50, 50], medium: [100, 100], large: [200, 200] }
  end

  def default_avatar
    "https://ui-avatars.com/api/?name=#{CGI.escape(full_name)}"
  end
end

# Usage in controllers/views
class UsersController < ApplicationController
  def show
    user = User.find(params[:id])
    @user = UserDecorator.new(user)
  end
end

# In view
<%= @user.full_name %>
<%= image_tag @user.avatar_url(size: :large) %>
<%= @user.membership_badge %>

# Advanced: Decorator with Draper gem
class PostDecorator < Draper::Decorator
  delegate_all

  def publication_status
    if published?
      h.content_tag :span, "Published", class: "badge badge-success"
    else
      h.content_tag :span, "Draft", class: "badge badge-secondary"
    end
  end

  def reading_time
    words = body.split.size
    minutes = (words / 200.0).ceil
    "#{minutes} min read"
  end

  def formatted_body
    h.markdown(body) # Using helper method
  end
end
```

**Testing Concerns:**
```ruby
RSpec.describe Trackable do
  let(:trackable_class) do
    Class.new(ApplicationRecord) do
      self.table_name = 'posts'
      include Trackable
      tracked_attributes :title
    end
  end

  let(:instance) { trackable_class.new(title: "Test") }

  describe "tracking creation" do
    it "creates activity on creation" do
      expect {
        instance.save!
      }.to change { instance.activities.count }.by(1)
    end
  end

  describe "tracking updates" do
    before { instance.save! }

    it "tracks attribute changes" do
      instance.update!(title: "Updated")

      activity = instance.activities.last
      expect(activity.event_type).to eq('updated')
      expect(activity.metadata['changes']).to include('title')
    end
  end
end
```

**Testing Decorators:**
```ruby
RSpec.describe UserDecorator do
  let(:user) { build(:user, first_name: "Alice", last_name: "Smith") }
  let(:decorated) { UserDecorator.new(user) }

  describe "#full_name" do
    it "combines first and last name" do
      expect(decorated.full_name).to eq("Alice Smith")
    end
  end

  describe "#membership_badge" do
    it "shows premium badge" do
      allow(user).to receive(:premium?).and_return(true)
      expect(decorated.membership_badge).to eq("👑 Premium")
    end
  end
end
```

---

### 3.4 Multi-Tenancy Patterns
**Difficulty:** Difficult
**When to Apply:** SaaS applications, data isolation by tenant

```ruby
# Approach 1: Schema-based (using apartment gem)
# Each tenant gets own PostgreSQL schema

# config/initializers/apartment.rb
Apartment.configure do |config|
  config.excluded_models = %w[Account User]
  config.tenant_names = -> { Account.pluck(:subdomain) }
end

# Middleware to switch tenant
class TenantMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    request = Rack::Request.new(env)
    subdomain = extract_subdomain(request.host)

    Apartment::Tenant.switch!(subdomain) do
      @app.call(env)
    end
  end

  private

  def extract_subdomain(host)
    host.split('.').first
  end
end

# Usage in controllers
class ApplicationController < ActionController::Base
  before_action :set_tenant

  private

  def set_tenant
    subdomain = request.subdomain
    Apartment::Tenant.switch!(subdomain)
  end
end

# Approach 2: Row-level (scoped by account_id)
module MultiTenant
  extend ActiveSupport::Concern

  included do
    belongs_to :account

    default_scope { where(account_id: Current.account_id) }

    validates :account_id, presence: true

    before_validation :set_account_id, on: :create
  end

  private

  def set_account_id
    self.account_id ||= Current.account_id
  end
end

# Current context using ActiveSupport::CurrentAttributes
class Current < ActiveSupport::CurrentAttributes
  attribute :account, :user

  def account_id
    account&.id
  end
end

# Usage in models
class Post < ApplicationRecord
  include MultiTenant
end

class Comment < ApplicationRecord
  include MultiTenant
  belongs_to :post
end

# Middleware to set current account
class AccountMiddleware
  def initialize(app)
    @app = app
  end

  def call(env)
    request = Rack::Request.new(env)
    subdomain = extract_subdomain(request.host)
    account = Account.find_by(subdomain: subdomain)

    Current.account = account

    @app.call(env)
  ensure
    Current.reset
  end

  private

  def extract_subdomain(host)
    host.split('.').first
  end
end

# Advanced: Hybrid approach with acts_as_tenant gem
class ApplicationRecord < ActiveRecord::Base
  self.abstract_class = true
end

class Post < ApplicationRecord
  acts_as_tenant(:account)
end

class PostsController < ApplicationController
  set_current_tenant_through_filter

  before_action :set_current_account

  def index
    @posts = Post.all # Automatically scoped to current account
  end

  private

  def set_current_account
    subdomain = request.subdomain
    set_current_tenant(Account.find_by!(subdomain: subdomain))
  end
end
```

**Testing Multi-Tenancy:**
```ruby
RSpec.describe Post, type: :model do
  let(:account1) { create(:account) }
  let(:account2) { create(:account) }

  describe "tenant isolation" do
    it "scopes queries to current account" do
      Current.account = account1
      post1 = create(:post, account: account1)

      Current.account = account2
      post2 = create(:post, account: account2)

      Current.account = account1
      expect(Post.all).to eq([post1])

      Current.account = account2
      expect(Post.all).to eq([post2])
    end
  end

  describe "cross-tenant access prevention" do
    it "prevents accessing other tenant's data" do
      Current.account = account1
      post = create(:post, account: account1)

      Current.account = account2
      expect(Post.find_by(id: post.id)).to be_nil
    end
  end
end
```

---

### 3.5 API Versioning Strategies
**Difficulty:** Moderate
**When to Apply:** Public APIs, breaking changes, backward compatibility

```ruby
# Approach 1: URL-based versioning
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :users
      resources :posts
    end

    namespace :v2 do
      resources :users
      resources :posts
    end
  end
end

# app/controllers/api/v1/users_controller.rb
module Api
  module V1
    class UsersController < ApiController
      def index
        users = User.all
        render json: users, each_serializer: V1::UserSerializer
      end
    end
  end
end

# app/controllers/api/v2/users_controller.rb
module Api
  module V2
    class UsersController < ApiController
      def index
        users = User.all
        render json: users, each_serializer: V2::UserSerializer
      end
    end
  end
end

# Approach 2: Header-based versioning
class ApiController < ApplicationController
  before_action :validate_api_version

  private

  def validate_api_version
    @api_version = request.headers['API-Version'] || 'v1'

    unless %w[v1 v2].include?(@api_version)
      render json: { error: 'Invalid API version' }, status: :not_acceptable
    end
  end

  def serializer_for(resource)
    "#{@api_version.camelize}::#{resource.class.name}Serializer".constantize
  end
end

class UsersController < ApiController
  def show
    user = User.find(params[:id])
    render json: user, serializer: serializer_for(user)
  end
end

# Approach 3: Accept header versioning (content negotiation)
class ApiController < ApplicationController
  before_action :set_api_version

  private

  def set_api_version
    accept_header = request.headers['Accept']

    @api_version = if accept_header&.include?('application/vnd.myapp.v2+json')
                     'v2'
                   elsif accept_header&.include?('application/vnd.myapp.v1+json')
                     'v1'
                   else
                     'v1' # default
                   end
  end
end

# Advanced: Version-specific serializers
module Api
  module V1
    class UserSerializer < ActiveModel::Serializer
      attributes :id, :name, :email

      def email
        object.email.downcase
      end
    end
  end

  module V2
    class UserSerializer < ActiveModel::Serializer
      attributes :id, :full_name, :contact

      def full_name
        "#{object.first_name} #{object.last_name}"
      end

      def contact
        {
          email: object.email,
          phone: object.phone
        }
      end
    end
  end
end

# Deprecation warnings
class ApiController < ApplicationController
  after_action :add_deprecation_header

  private

  def add_deprecation_header
    if @api_version == 'v1'
      response.headers['X-API-Deprecation'] = 'v1 will be deprecated on 2026-01-01'
      response.headers['X-API-Sunset'] = '2026-01-01'
    end
  end
end
```

**Testing API Versions:**
```ruby
RSpec.describe "API V1 Users", type: :request do
  describe "GET /api/v1/users/:id" do
    let(:user) { create(:user, name: "Alice", email: "ALICE@EXAMPLE.COM") }

    it "returns user with v1 format" do
      get "/api/v1/users/#{user.id}"

      expect(response).to have_http_status(:success)
      json = JSON.parse(response.body)
      expect(json['email']).to eq('alice@example.com') # Lowercased in v1
    end
  end
end

RSpec.describe "API V2 Users", type: :request do
  describe "GET /api/v2/users/:id" do
    let(:user) { create(:user, first_name: "Alice", last_name: "Smith") }

    it "returns user with v2 format" do
      get "/api/v2/users/#{user.id}"

      expect(response).to have_http_status(:success)
      json = JSON.parse(response.body)
      expect(json['full_name']).to eq('Alice Smith')
      expect(json['contact']).to include('email', 'phone')
    end
  end
end
```

---

## 4. Testing Excellence

### 4.1 RSpec Best Practices
**Difficulty:** Moderate
**When to Apply:** All test scenarios, maintainable test suites

```ruby
# Good: Descriptive context and examples
RSpec.describe User do
  describe "#activate" do
    let(:user) { create(:user, activated: false) }

    context "when user is inactive" do
      it "activates the user" do
        expect { user.activate }.to change(user, :activated).from(false).to(true)
      end

      it "sets activation timestamp" do
        user.activate
        expect(user.activated_at).to be_within(1.second).of(Time.current)
      end

      it "sends activation email" do
        expect {
          user.activate
        }.to have_enqueued_mail(UserMailer, :activation_confirmation)
      end
    end

    context "when user is already active" do
      before { user.update!(activated: true) }

      it "does not change activation status" do
        expect { user.activate }.not_to change(user, :activated)
      end

      it "does not send email" do
        expect { user.activate }.not_to have_enqueued_mail
      end
    end
  end
end

# Advanced: Shared examples for DRY tests
RSpec.shared_examples "a trackable model" do
  it "creates activity on creation" do
    expect {
      described_class.create!(valid_attributes)
    }.to change(Activity, :count).by(1)
  end

  it "tracks updates" do
    record = described_class.create!(valid_attributes)

    expect {
      record.update!(update_attributes)
    }.to change { record.activities.count }.by(1)
  end
end

RSpec.describe Post do
  it_behaves_like "a trackable model" do
    let(:valid_attributes) { { title: "Test", body: "Content" } }
    let(:update_attributes) { { title: "Updated" } }
  end
end

RSpec.describe User do
  it_behaves_like "a trackable model" do
    let(:valid_attributes) { { name: "Alice", email: "alice@example.com" } }
    let(:update_attributes) { { name: "Bob" } }
  end
end

# Advanced: Custom matchers
RSpec::Matchers.define :have_error_on do |attribute|
  match do |model|
    model.valid?
    model.errors[attribute].any?
  end

  failure_message do |model|
    "expected #{model.class} to have error on #{attribute}, but it didn't"
  end
end

# Usage
RSpec.describe User do
  it "validates email presence" do
    user = User.new(email: nil)
    expect(user).to have_error_on(:email)
  end
end

# Performance testing with benchmark matchers
RSpec.describe "Query performance" do
  it "loads users efficiently" do
    create_list(:user, 100, :with_posts)

    expect {
      User.includes(:posts).to_a
    }.to perform_under(100).ms
  end

  it "prevents N+1 queries" do
    create_list(:user, 10, :with_posts)

    expect {
      User.includes(:posts).each { |u| u.posts.to_a }
    }.to make_database_queries(count: 2)
  end
end
```

---

### 4.2 Factory Patterns with FactoryBot
**Difficulty:** Moderate
**When to Apply:** Test data creation, realistic scenarios

```ruby
# Basic factory
FactoryBot.define do
  factory :user do
    sequence(:email) { |n| "user#{n}@example.com" }
    name { "John Doe" }
    password { "password123" }

    trait :admin do
      role { :admin }
    end

    trait :with_posts do
      after(:create) do |user|
        create_list(:post, 3, user: user)
      end
    end

    trait :activated do
      activated { true }
      activated_at { Time.current }
    end

    factory :admin_user, traits: [:admin, :activated]
  end
end

# Advanced: Nested factories
FactoryBot.define do
  factory :post do
    association :user
    sequence(:title) { |n| "Post #{n}" }
    body { "Post content here" }
    status { :draft }

    trait :published do
      status { :published }
      published_at { Time.current }
    end

    trait :with_comments do
      after(:create) do |post|
        create_list(:comment, 5, post: post)
      end
    end

    trait :with_tags do
      after(:create) do |post|
        create_list(:tag, 3, posts: [post])
      end
    end

    factory :published_post, traits: [:published, :with_comments]
  end
end

# Dynamic attributes
FactoryBot.define do
  factory :order do
    association :user

    transient do
      items_count { 3 }
    end

    after(:create) do |order, evaluator|
      create_list(:order_item, evaluator.items_count, order: order)
    end

    trait :with_discount do
      after(:create) do |order|
        order.apply_discount!(10)
      end
    end
  end
end

# Usage
user = create(:user, :admin, :with_posts)
post = create(:post, :published, user: user)
order = create(:order, items_count: 5, :with_discount)

# Using build_stubbed for performance
user = build_stubbed(:user) # Doesn't hit database
```

**Testing with Factories:**
```ruby
RSpec.describe Post do
  describe "associations" do
    it "belongs to user" do
      post = build(:post)
      expect(post.user).to be_a(User)
    end
  end

  describe "publishing" do
    let(:post) { create(:post, :draft) }

    it "changes status to published" do
      expect {
        post.publish!
      }.to change(post, :status).from(:draft).to(:published)
    end
  end

  describe "with_comments trait" do
    let(:post) { create(:post, :with_comments) }

    it "creates post with 5 comments" do
      expect(post.comments.count).to eq(5)
    end
  end
end
```

---

### 4.3 Test Doubles and Mocking
**Difficulty:** Moderate
**When to Apply:** External dependencies, isolation, performance

```ruby
# Doubles for isolation
RSpec.describe UserService do
  let(:email_service) { instance_double(EmailService) }
  let(:service) { UserService.new(email_service: email_service) }

  describe "#register" do
    let(:user_params) { { email: "alice@example.com", name: "Alice" } }

    before do
      allow(email_service).to receive(:send_welcome).and_return(true)
    end

    it "sends welcome email" do
      service.register(user_params)
      expect(email_service).to have_received(:send_welcome).with("alice@example.com", "Alice")
    end

    context "when email fails" do
      before do
        allow(email_service).to receive(:send_welcome).and_raise(EmailService::Error)
      end

      it "handles error gracefully" do
        expect {
          service.register(user_params)
        }.not_to raise_error
      end
    end
  end
end

# Stubbing for external APIs
RSpec.describe PaymentService do
  describe "#charge" do
    let(:gateway) { instance_double(PaymentGateway) }
    let(:service) { PaymentService.new(gateway: gateway) }

    context "when payment succeeds" do
      let(:successful_response) { double(success?: true, id: "ch_123") }

      before do
        allow(gateway).to receive(:charge).and_return(successful_response)
      end

      it "returns success" do
        result = service.charge(amount: 100, token: "tok_abc")
        expect(result).to be_success
      end
    end

    context "when payment fails" do
      let(:failed_response) { double(success?: false, error: "Card declined") }

      before do
        allow(gateway).to receive(:charge).and_return(failed_response)
      end

      it "returns failure with error" do
        result = service.charge(amount: 100, token: "tok_abc")
        expect(result).to be_failure
        expect(result.error).to eq("Card declined")
      end
    end
  end
end

# Spies for after-the-fact verification
RSpec.describe NotificationService do
  let(:logger) { spy("Logger") }
  let(:service) { NotificationService.new(logger: logger) }

  it "logs notification sent" do
    service.send_notification(user_id: 1, message: "Hello")

    expect(logger).to have_received(:info).with(/Notification sent/)
  end
end

# Verifying doubles (strict doubles that verify method existence)
RSpec.describe UserController do
  let(:user_service) { instance_double(UserService, register: true) }

  before do
    allow(UserService).to receive(:new).and_return(user_service)
  end

  it "calls register on service" do
    post :create, params: { user: { email: "test@example.com" } }
    expect(user_service).to have_received(:register)
  end
end
```

---

### 4.4 Integration Testing Strategies
**Difficulty:** Moderate to Difficult
**When to Apply:** End-to-end flows, API testing, critical paths

```ruby
# Request specs for API testing
RSpec.describe "Users API", type: :request do
  describe "POST /api/users" do
    let(:valid_params) do
      {
        user: {
          email: "alice@example.com",
          name: "Alice",
          password: "password123"
        }
      }
    end

    context "with valid params" do
      it "creates user" do
        expect {
          post "/api/users", params: valid_params
        }.to change(User, :count).by(1)
      end

      it "returns created status" do
        post "/api/users", params: valid_params
        expect(response).to have_http_status(:created)
      end

      it "returns user JSON" do
        post "/api/users", params: valid_params
        json = JSON.parse(response.body)
        expect(json['email']).to eq("alice@example.com")
      end
    end

    context "with invalid params" do
      let(:invalid_params) { { user: { email: "" } } }

      it "does not create user" do
        expect {
          post "/api/users", params: invalid_params
        }.not_to change(User, :count)
      end

      it "returns unprocessable entity" do
        post "/api/users", params: invalid_params
        expect(response).to have_http_status(:unprocessable_entity)
      end

      it "returns error messages" do
        post "/api/users", params: invalid_params
        json = JSON.parse(response.body)
        expect(json['errors']).to include('email')
      end
    end
  end

  describe "authentication" do
    let(:user) { create(:user, password: "password123") }

    describe "POST /api/login" do
      it "returns JWT token" do
        post "/api/login", params: { email: user.email, password: "password123" }

        expect(response).to have_http_status(:ok)
        json = JSON.parse(response.body)
        expect(json['token']).to be_present
      end
    end

    describe "protected endpoints" do
      let(:token) { JWT.encode({ user_id: user.id }, Rails.application.secret_key_base) }

      it "allows access with valid token" do
        get "/api/profile", headers: { "Authorization" => "Bearer #{token}" }
        expect(response).to have_http_status(:ok)
      end

      it "denies access without token" do
        get "/api/profile"
        expect(response).to have_http_status(:unauthorized)
      end
    end
  end
end

# System specs with Capybara
RSpec.describe "User registration", type: :system do
  before do
    driven_by(:selenium_chrome_headless)
  end

  it "allows new user to register" do
    visit root_path
    click_link "Sign Up"

    fill_in "Email", with: "alice@example.com"
    fill_in "Name", with: "Alice"
    fill_in "Password", with: "password123"
    fill_in "Password confirmation", with: "password123"

    click_button "Create Account"

    expect(page).to have_content("Welcome, Alice!")
    expect(page).to have_current_path(dashboard_path)
  end

  it "shows validation errors" do
    visit new_user_path

    click_button "Create Account"

    expect(page).to have_content("Email can't be blank")
    expect(page).to have_content("Password can't be blank")
  end
end

# Feature specs for complex workflows
RSpec.describe "Order checkout flow", type: :feature do
  let(:user) { create(:user) }
  let(:product) { create(:product, price: 29.99) }

  before do
    login_as(user)
  end

  it "completes full checkout" do
    # Add to cart
    visit product_path(product)
    click_button "Add to Cart"
    expect(page).to have_content("Item added to cart")

    # View cart
    click_link "Cart"
    expect(page).to have_content(product.name)
    expect(page).to have_content("$29.99")

    # Checkout
    click_button "Checkout"

    # Fill shipping
    fill_in "Street", with: "123 Main St"
    fill_in "City", with: "New York"
    fill_in "Zip", with: "10001"
    click_button "Continue"

    # Fill payment
    fill_in "Card number", with: "4242424242424242"
    fill_in "Expiry", with: "12/25"
    fill_in "CVV", with: "123"
    click_button "Place Order"

    # Confirmation
    expect(page).to have_content("Order confirmed")
    expect(page).to have_content("Order #")
  end
end
```

---

### 4.5 Contract Testing
**Difficulty:** Difficult
**When to Apply:** Microservices, external APIs, consumer-provider contracts

```ruby
# Using Pact for consumer-driven contract testing

# Consumer side (API client)
RSpec.describe UserServiceClient, pact: true do
  let(:user_service) { UserServiceClient.new }

  describe "get user" do
    before do
      user_service.given("user 1 exists")
        .upon_receiving("a request for user 1")
        .with(method: :get, path: "/users/1", headers: { "Accept" => "application/json" })
        .will_respond_with(
          status: 200,
          headers: { "Content-Type" => "application/json" },
          body: {
            id: 1,
            name: "Alice",
            email: "alice@example.com"
          }
        )
    end

    it "returns user details" do
      user = user_service.get_user(1)
      expect(user.name).to eq("Alice")
      expect(user.email).to eq("alice@example.com")
    end
  end

  describe "create user" do
    let(:user_params) { { name: "Bob", email: "bob@example.com" } }

    before do
      user_service.given("no user exists")
        .upon_receiving("a request to create user")
        .with(
          method: :post,
          path: "/users",
          headers: { "Content-Type" => "application/json" },
          body: user_params
        )
        .will_respond_with(
          status: 201,
          headers: { "Content-Type" => "application/json" },
          body: {
            id: 2,
            name: "Bob",
            email: "bob@example.com"
          }
        )
    end

    it "creates user" do
      user = user_service.create_user(user_params)
      expect(user.id).to eq(2)
      expect(user.name).to eq("Bob")
    end
  end
end

# Provider side (API verification)
RSpec.describe "User API contract", type: :request, pact: true do
  let(:user) { create(:user, id: 1, name: "Alice", email: "alice@example.com") }

  describe "get user" do
    it "verifies contract" do
      get "/users/#{user.id}", headers: { "Accept" => "application/json" }

      expect(response).to have_http_status(:ok)
      expect(response.content_type).to eq("application/json")

      json = JSON.parse(response.body)
      expect(json).to match(
        "id" => user.id,
        "name" => user.name,
        "email" => user.email
      )
    end
  end
end

# Schema validation for API contracts
RSpec.describe "API schema validation", type: :request do
  let(:user_schema) do
    {
      type: "object",
      required: ["id", "name", "email"],
      properties: {
        id: { type: "integer" },
        name: { type: "string" },
        email: { type: "string", format: "email" }
      }
    }
  end

  describe "GET /api/users/:id" do
    let(:user) { create(:user) }

    it "returns valid schema" do
      get "/api/users/#{user.id}"

      expect(response.body).to match_json_schema(user_schema)
    end
  end
end
```

---

## 5. Concurrent Programming

### 5.1 Thread Safety Patterns
**Difficulty:** Difficult
**When to Apply:** Multi-threaded environments, shared state, race conditions

```ruby
# Thread-safe singleton with double-checked locking
class Configuration
  @instance = nil
  @mutex = Mutex.new

  def self.instance
    return @instance if @instance

    @mutex.synchronize do
      @instance ||= new
    end
  end

  private_class_method :new

  def initialize
    @settings = {}
    @mutex = Mutex.new
  end

  def get(key)
    @mutex.synchronize { @settings[key] }
  end

  def set(key, value)
    @mutex.synchronize { @settings[key] = value }
  end
end

# Thread-safe cache with concurrent-ruby
require 'concurrent'

class ThreadSafeCache
  def initialize
    @cache = Concurrent::Map.new
  end

  def fetch(key, &block)
    @cache.fetch_or_store(key) do
      block.call if block_given?
    end
  end

  def get(key)
    @cache[key]
  end

  def set(key, value)
    @cache[key] = value
  end

  def delete(key)
    @cache.delete(key)
  end

  def clear
    @cache.clear
  end
end

# Usage
cache = ThreadSafeCache.new

threads = 10.times.map do
  Thread.new do
    cache.fetch("expensive_computation") do
      # This block runs only once, even with multiple threads
      sleep 1
      "result"
    end
  end
end

threads.each(&:join)

# Atomic operations for counters
class AtomicCounter
  def initialize(initial = 0)
    @count = Concurrent::AtomicFixnum.new(initial)
  end

  def increment
    @count.increment
  end

  def decrement
    @count.decrement
  end

  def value
    @count.value
  end
end

# Thread pool for controlled concurrency
pool = Concurrent::FixedThreadPool.new(5)

100.times do |i|
  pool.post do
    # Task executed in thread pool
    puts "Processing task #{i} in thread #{Thread.current.object_id}"
    sleep rand
  end
end

pool.shutdown
pool.wait_for_termination

# Future for async computation
future = Concurrent::Future.execute do
  # Long-running computation
  sleep 2
  "result"
end

# Do other work...

puts future.value # Blocks until result is ready

# Promise for manual completion
promise = Concurrent::Promise.new

Thread.new do
  sleep 1
  promise.set("result")
end

puts promise.value # Blocks until promise is fulfilled
```

**Rails-specific Thread Safety:**
```ruby
# Thread-safe Rails background task
class ThreadSafeProcessor
  def self.process_batch(items)
    # Create new connection pool for threads
    ActiveRecord::Base.connection_pool.with_connection do
      threads = items.map do |item|
        Thread.new do
          # Each thread gets its own connection
          ActiveRecord::Base.connection_pool.with_connection do
            process_item(item)
          end
        end
      end

      threads.each(&:join)
    end
  end

  def self.process_item(item)
    # Thread-safe item processing
    item.update!(processed: true)
  end
end
```

**Testing Thread Safety:**
```ruby
RSpec.describe ThreadSafeCache do
  let(:cache) { ThreadSafeCache.new }

  describe "concurrent access" do
    it "handles concurrent writes" do
      threads = 100.times.map do |i|
        Thread.new { cache.set("key#{i}", "value#{i}") }
      end

      threads.each(&:join)

      expect(cache.get("key99")).to eq("value99")
    end

    it "prevents race conditions in fetch" do
      call_count = Concurrent::AtomicFixnum.new(0)

      threads = 10.times.map do
        Thread.new do
          cache.fetch("shared_key") do
            call_count.increment
            "result"
          end
        end
      end

      threads.each(&:join)

      expect(call_count.value).to eq(1) # Block called only once
    end
  end
end
```

---

### 5.2 Fiber Usage for Cooperative Concurrency
**Difficulty:** Moderate
**When to Apply:** Cooperative multitasking, generators, lightweight concurrency

```ruby
# Basic fiber for lazy evaluation
fibonacci = Fiber.new do
  a, b = 0, 1

  loop do
    Fiber.yield a
    a, b = b, a + b
  end
end

10.times { puts fibonacci.resume } # 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

# Fiber-based generator
class Generator
  def initialize(&block)
    @fiber = Fiber.new(&block)
  end

  def next
    @fiber.resume
  end

  def each(&block)
    loop do
      value = self.next
      break if value.nil?
      block.call(value)
    end
  end
end

# Usage
range = Generator.new do
  10.times do |i|
    Fiber.yield i * 2
  end
end

range.each { |n| puts n } # 0, 2, 4, 6, 8, 10, 12, 14, 16, 18

# Fiber pool for IO-bound tasks
class FiberPool
  def initialize(size)
    @size = size
    @fibers = []
  end

  def spawn(&block)
    if @fibers.size < @size
      fiber = Fiber.new do
        loop do
          task = Fiber.yield
          break unless task
          task.call
        end
      end

      @fibers << fiber
      fiber.resume
    end

    @fibers.first.resume(block)
    @fibers.rotate!
  end

  def shutdown
    @fibers.each { |f| f.resume(nil) }
  end
end

# Usage
pool = FiberPool.new(5)

10.times do |i|
  pool.spawn do
    puts "Task #{i} executed in fiber #{Fiber.current.object_id}"
  end
end

pool.shutdown

# Fiber for streaming large datasets
class StreamProcessor
  def self.process_large_file(filename)
    Fiber.new do
      File.foreach(filename) do |line|
        Fiber.yield line.chomp
      end
    end
  end
end

# Usage
fiber = StreamProcessor.process_large_file("large_file.txt")

while (line = fiber.resume)
  # Process line without loading entire file into memory
  puts line
end
```

---

### 5.3 Ractor Patterns (Ruby 3+)
**Difficulty:** Difficult
**When to Apply:** Parallel processing, CPU-bound tasks, true parallelism

```ruby
# Basic Ractor for parallel computation
def parallel_map(array, &block)
  ractors = array.map do |item|
    Ractor.new(item, block) do |value, fn|
      fn.call(value)
    end
  end

  ractors.map(&:take)
end

# Usage
numbers = [1, 2, 3, 4, 5]
results = parallel_map(numbers) { |n| n * 2 }
puts results.inspect # [2, 4, 6, 8, 10]

# Ractor pipeline for data processing
class Pipeline
  def initialize(*stages)
    @stages = stages
  end

  def process(input)
    ractors = @stages.map.with_index do |stage, index|
      Ractor.new(stage, index) do |fn, idx|
        loop do
          data = receive
          result = fn.call(data)
          Ractor.yield result
        end
      end
    end

    # Send input to first ractor
    ractors.first.send(input)

    # Pipe data through stages
    (ractors.size - 1).times do |i|
      data = ractors[i].take
      ractors[i + 1].send(data)
    end

    # Get final result
    ractors.last.take
  end
end

# Usage
pipeline = Pipeline.new(
  ->(x) { x * 2 },      # Stage 1: double
  ->(x) { x + 10 },     # Stage 2: add 10
  ->(x) { x.to_s }      # Stage 3: convert to string
)

result = pipeline.process(5) # "20"

# Worker pool with Ractors
class WorkerPool
  def initialize(worker_count)
    @workers = worker_count.times.map do |i|
      Ractor.new(i) do |id|
        loop do
          task = Ractor.receive
          result = task.call
          Ractor.yield [id, result]
        end
      end
    end
  end

  def submit(&task)
    worker = @workers.sample
    worker.send(task)
  end

  def results(count)
    count.times.map do
      Ractor.select(*@workers).last
    end
  end
end

# Usage
pool = WorkerPool.new(4)

10.times do |i|
  pool.submit { "Task #{i} completed" }
end

results = pool.results(10)
results.each { |worker_id, result| puts "[Worker #{worker_id}] #{result}" }
```

**Performance Implications:**
- Ractors provide true parallelism (bypasses GIL)
- Each Ractor has isolated memory (no shared state)
- Communication via message passing (copy overhead)
- Best for CPU-bound tasks, not IO-bound

---

### 5.4 Concurrent Data Structures
**Difficulty:** Moderate
**When to Apply:** Multi-threaded applications, shared state management

```ruby
require 'concurrent'

# Concurrent::Map for thread-safe hash
class UserCache
  def initialize
    @cache = Concurrent::Map.new
  end

  def fetch_user(id)
    @cache.fetch_or_store(id) do
      # Expensive database query, runs only once per ID
      User.find(id)
    end
  end

  def invalidate(id)
    @cache.delete(id)
  end

  def clear
    @cache.clear
  end
end

# Concurrent::Array for thread-safe array operations
class EventCollector
  def initialize
    @events = Concurrent::Array.new
  end

  def record(event)
    @events << event
  end

  def events
    @events.to_a
  end

  def count
    @events.size
  end
end

# Usage with threads
collector = EventCollector.new

threads = 100.times.map do |i|
  Thread.new { collector.record("Event #{i}") }
end

threads.each(&:join)
puts collector.count # 100

# Concurrent::Hash for complex concurrent operations
class RequestCounter
  def initialize
    @counts = Concurrent::Hash.new(0)
  end

  def increment(path)
    @counts.compute(path) { |count| count + 1 }
  end

  def get(path)
    @counts[path]
  end

  def top(n = 10)
    @counts.sort_by { |_, count| -count }.first(n).to_h
  end
end

# Lock-free data structures
class LockFreeStack
  def initialize
    @head = Concurrent::AtomicReference.new(nil)
  end

  def push(value)
    loop do
      old_head = @head.get
      new_node = Node.new(value, old_head)

      # Atomic compare-and-swap
      break if @head.compare_and_set(old_head, new_node)
    end
  end

  def pop
    loop do
      old_head = @head.get
      return nil unless old_head

      new_head = old_head.next

      if @head.compare_and_set(old_head, new_head)
        return old_head.value
      end
    end
  end

  Node = Struct.new(:value, :next)
end
```

---

## Summary and Recommendations

### Difficulty Ratings Summary
- **Moderate:** Service Objects, Query Objects, Form Objects, Repository Pattern, RSpec, FactoryBot, Thread Safety Basics, Fiber Usage
- **Difficult:** Metaprogramming (eigenclass, refinements), Interactor Pattern, Multi-Tenancy, Contract Testing, Ractor Patterns

### Performance Considerations
1. **Metaprogramming:** Use `define_method` over `method_missing` when possible
2. **ActiveRecord:** Always use `includes`/`preload` to prevent N+1 queries
3. **Background Jobs:** Implement idempotency and exponential backoff
4. **Concurrency:** Use Ractors for CPU-bound, Fibers for IO-bound tasks

### Testing Best Practices
1. Use factories with traits for flexible test data
2. Mock external dependencies, but avoid over-mocking
3. Write integration tests for critical paths
4. Use contract testing for microservices

### When to Use Each Pattern
- **Service Objects:** Complex multi-step operations
- **Interactors:** Workflows requiring rollback capability
- **Query Objects:** Complex database queries, reusable filters
- **Form Objects:** Multi-model forms, complex validations
- **Repository Pattern:** Data access abstraction, testing without DB

### Rails-Specific Recommendations
1. Use concerns for shared model behavior
2. Implement decorators for presentation logic
3. Choose multi-tenancy strategy based on isolation needs
4. Version APIs early, even for internal services
5. Optimize queries before adding caching

---

## References and Further Reading

- **Metaprogramming Ruby 2** by Paolo Perrotta
- **Confident Ruby** by Avdi Grimm
- **Rails AntiPatterns** by Chad Pytel and Tammer Saleh
- **Concurrent Programming in Ruby** (Pragmatic Programmers)
- **Effective Testing with RSpec 3** by Myron Marston

---

**End of Research Document**
